/**
 * Mobile-First Schedule Screen
 * Touch-friendly schedule display with premium visual elements
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useDispatch, useSelector } from 'react-redux';

import { RootState } from '../store/store';
import { fetchSchedule } from '../store/slices/scheduleSlice';

const { width } = Dimensions.get('window');

interface ScheduleItem {
  id: string;
  title: string;
  time: string;
  duration: number;
  type: 'task' | 'meeting' | 'break' | 'focus' | 'health';
  priority: 'high' | 'medium' | 'low';
  completed: boolean;
  description?: string;
}

const ScheduleScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { todaySchedule, loading } = useSelector((state: RootState) => state.schedule);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedDate, setSelectedDate] = useState(new Date());

  useEffect(() => {
    loadSchedule();
  }, [selectedDate]);

  const loadSchedule = async () => {
    try {
      // @ts-ignore
      await dispatch(fetchSchedule({ date: selectedDate.toISOString() }));
    } catch (error) {
      console.error('Failed to load schedule:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadSchedule();
    setRefreshing(false);
  };

  const getTypeColor = (type: string) => {
    const colors = {
      task: ['#4CAF50', '#8BC34A'],
      meeting: ['#2196F3', '#03DAC6'],
      break: ['#FF9800', '#FF5722'],
      focus: ['#9C27B0', '#E91E63'],
      health: ['#FF6B35', '#F7931E'],
    };
    return colors[type as keyof typeof colors] || colors.task;
  };

  const getTypeIcon = (type: string) => {
    const icons = {
      task: 'checkmark-circle',
      meeting: 'people',
      break: 'cafe',
      focus: 'flash',
      health: 'fitness',
    };
    return icons[type as keyof typeof icons] || 'checkmark-circle';
  };

  const renderDateSelector = () => (
    <View style={styles.dateSelector}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {Array.from({ length: 7 }, (_, i) => {
          const date = new Date();
          date.setDate(date.getDate() + i);
          const isSelected = date.toDateString() === selectedDate.toDateString();
          
          return (
            <TouchableOpacity
              key={i}
              style={[styles.dateItem, isSelected && styles.selectedDateItem]}
              onPress={() => setSelectedDate(date)}
            >
              <Text style={[styles.dayText, isSelected && styles.selectedDayText]}>
                {date.toLocaleDateString('en', { weekday: 'short' })}
              </Text>
              <Text style={[styles.dateText, isSelected && styles.selectedDateText]}>
                {date.getDate()}
              </Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>
    </View>
  );

  const renderScheduleItem = (item: ScheduleItem, index: number) => (
    <TouchableOpacity key={item.id} style={styles.scheduleItem}>
      <LinearGradient
        colors={getTypeColor(item.type)}
        style={styles.scheduleItemGradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        <View style={styles.scheduleItemContent}>
          <View style={styles.scheduleItemHeader}>
            <View style={styles.scheduleItemInfo}>
              <Ionicons 
                name={getTypeIcon(item.type) as any} 
                size={20} 
                color="#FFFFFF" 
              />
              <Text style={styles.scheduleItemTime}>{item.time}</Text>
            </View>
            <View style={styles.priorityIndicator}>
              <View style={[
                styles.priorityDot,
                { backgroundColor: item.priority === 'high' ? '#FF4444' : 
                                 item.priority === 'medium' ? '#FFA500' : '#4CAF50' }
              ]} />
            </View>
          </View>
          
          <Text style={styles.scheduleItemTitle}>{item.title}</Text>
          
          {item.description && (
            <Text style={styles.scheduleItemDescription} numberOfLines={2}>
              {item.description}
            </Text>
          )}
          
          <View style={styles.scheduleItemFooter}>
            <Text style={styles.scheduleItemDuration}>
              {item.duration} min
            </Text>
            {item.completed && (
              <Ionicons name="checkmark-circle" size={20} color="#FFFFFF" />
            )}
          </View>
        </View>
      </LinearGradient>
    </TouchableOpacity>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Ionicons name="calendar-outline" size={64} color="#CCCCCC" />
      <Text style={styles.emptyStateTitle}>No Schedule Items</Text>
      <Text style={styles.emptyStateText}>
        Your schedule for this day is clear. Time to plan something amazing!
      </Text>
      <TouchableOpacity style={styles.addButton}>
        <LinearGradient
          colors={['#FF6B35', '#F7931E']}
          style={styles.addButtonGradient}
        >
          <Ionicons name="add" size={24} color="#FFFFFF" />
          <Text style={styles.addButtonText}>Add Task</Text>
        </LinearGradient>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Schedule</Text>
        <TouchableOpacity style={styles.headerButton}>
          <Ionicons name="add" size={24} color="#FF6B35" />
        </TouchableOpacity>
      </View>

      {renderDateSelector()}

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        {todaySchedule && todaySchedule.length > 0 ? (
          <View style={styles.scheduleList}>
            {todaySchedule.map((item, index) => renderScheduleItem(item, index))}
          </View>
        ) : (
          renderEmptyState()
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1A1A1A',
  },
  headerButton: {
    padding: 8,
  },
  dateSelector: {
    backgroundColor: '#FFFFFF',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  dateItem: {
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    marginHorizontal: 4,
    borderRadius: 12,
    minWidth: 60,
  },
  selectedDateItem: {
    backgroundColor: '#FF6B35',
  },
  dayText: {
    fontSize: 12,
    color: '#8E8E93',
    marginBottom: 4,
  },
  selectedDayText: {
    color: '#FFFFFF',
  },
  dateText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1A1A1A',
  },
  selectedDateText: {
    color: '#FFFFFF',
  },
  scrollView: {
    flex: 1,
  },
  scheduleList: {
    padding: 16,
  },
  scheduleItem: {
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  scheduleItemGradient: {
    padding: 16,
  },
  scheduleItemContent: {
    flex: 1,
  },
  scheduleItemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  scheduleItemInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scheduleItemTime: {
    fontSize: 14,
    color: '#FFFFFF',
    marginLeft: 8,
    fontWeight: '600',
  },
  priorityIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  scheduleItemTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  scheduleItemDescription: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    marginBottom: 8,
    lineHeight: 20,
  },
  scheduleItemFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  scheduleItemDuration: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.8,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 32,
    paddingVertical: 64,
  },
  emptyStateTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#8E8E93',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
  },
  addButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  addButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  addButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 8,
  },
});

export default ScheduleScreen;