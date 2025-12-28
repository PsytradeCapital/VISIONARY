/**
 * Progress Screen with Photorealistic Progress Visualization
 * Interactive charts with photorealistic background images
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
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useDispatch, useSelector } from 'react-redux';

import { RootState } from '../store/store';
import { fetchAnalytics } from '../store/slices/analyticsSlice';
import { aiImageService } from '../services/AIImageService';

const { width } = Dimensions.get('window');

interface ProgressCategory {
  id: string;
  title: string;
  progress: number;
  target: number;
  unit: string;
  color: string[];
  icon: string;
  imageUrl?: string;
  trend: 'up' | 'down' | 'stable';
  change: number;
}

const ProgressScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { analytics, loading } = useSelector((state: RootState) => state.analytics);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState<'week' | 'month' | 'year'>('week');
  const [progressImages, setProgressImages] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    loadProgressData();
    loadProgressImages();
  }, [selectedPeriod]);

  const loadProgressData = async () => {
    try {
      // @ts-ignore
      await dispatch(fetchAnalytics({ period: selectedPeriod }));
    } catch (error) {
      console.error('Failed to load progress data:', error);
    }
  };

  const loadProgressImages = async () => {
    try {
      const images = await Promise.all([
        aiImageService.generatePhotorealisticImage({
          category: 'health',
          style: 'real_people_exercising',
          context: 'real people achieving health goals, fit people exercising, healthy lifestyle',
          quality: 'hd'
        }),
        aiImageService.generatePhotorealisticImage({
          category: 'nutrition',
          style: 'healthy_food_photography',
          context: 'real nutritious meals, fresh healthy food, professional food photography',
          quality: 'hd'
        }),
        aiImageService.generatePhotorealisticImage({
          category: 'financial',
          style: 'success_environments',
          context: 'real financial success scenarios, people celebrating achievements',
          quality: 'hd'
        }),
        aiImageService.generatePhotorealisticImage({
          category: 'productivity',
          style: 'achievement_celebrations',
          context: 'real people achieving productivity goals, successful work environment',
          quality: 'hd'
        })
      ]);

      setProgressImages({
        health: images[0]?.url || aiImageService.getFallbackImage('health'),
        nutrition: images[1]?.url || aiImageService.getFallbackImage('nutrition'),
        financial: images[2]?.url || aiImageService.getFallbackImage('financial'),
        productivity: images[3]?.url || aiImageService.getFallbackImage('productivity')
      });
    } catch (error) {
      console.error('Failed to load progress images:', error);
      // Use fallback images
      setProgressImages({
        health: aiImageService.getFallbackImage('health'),
        nutrition: aiImageService.getFallbackImage('nutrition'),
        financial: aiImageService.getFallbackImage('financial'),
        productivity: aiImageService.getFallbackImage('productivity')
      });
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadProgressData();
    await loadProgressImages();
    setRefreshing(false);
  };

  const progressCategories: ProgressCategory[] = [
    {
      id: 'health',
      title: 'Health Goals',
      progress: analytics?.healthProgress || 65,
      target: 100,
      unit: '%',
      color: ['#FF6B35', '#F7931E'],
      icon: 'fitness',
      imageUrl: progressImages.health,
      trend: 'up',
      change: 12
    },
    {
      id: 'nutrition',
      title: 'Nutrition',
      progress: analytics?.nutritionProgress || 78,
      target: 100,
      unit: '%',
      color: ['#4CAF50', '#8BC34A'],
      icon: 'nutrition',
      imageUrl: progressImages.nutrition,
      trend: 'up',
      change: 8
    },
    {
      id: 'financial',
      title: 'Financial Goals',
      progress: analytics?.financialProgress || 45,
      target: 100,
      unit: '%',
      color: ['#2196F3', '#03DAC6'],
      icon: 'trending-up',
      imageUrl: progressImages.financial,
      trend: 'stable',
      change: 2
    },
    {
      id: 'productivity',
      title: 'Productivity',
      progress: analytics?.productivityScore || 82,
      target: 100,
      unit: '%',
      color: ['#9C27B0', '#E91E63'],
      icon: 'checkmark-circle',
      imageUrl: progressImages.productivity,
      trend: 'up',
      change: 15
    }
  ];

  const renderPeriodSelector = () => (
    <View style={styles.periodSelector}>
      {(['week', 'month', 'year'] as const).map((period) => (
        <TouchableOpacity
          key={period}
          style={[
            styles.periodButton,
            selectedPeriod === period && styles.selectedPeriodButton
          ]}
          onPress={() => setSelectedPeriod(period)}
        >
          <Text style={[
            styles.periodButtonText,
            selectedPeriod === period && styles.selectedPeriodButtonText
          ]}>
            {period.charAt(0).toUpperCase() + period.slice(1)}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderOverallProgress = () => {
    const overallProgress = progressCategories.reduce((sum, cat) => sum + cat.progress, 0) / progressCategories.length;
    
    return (
      <View style={styles.overallProgressCard}>
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.overallProgressGradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.overallProgressContent}>
            <Text style={styles.overallProgressTitle}>Overall Progress</Text>
            <Text style={styles.overallProgressValue}>{overallProgress.toFixed(0)}%</Text>
            <Text style={styles.overallProgressSubtitle}>
              Great momentum this {selectedPeriod}!
            </Text>
          </View>
          <View style={styles.overallProgressChart}>
            <View style={styles.progressRing}>
              <View style={[
                styles.progressRingFill,
                { 
                  transform: [{ rotate: `${(overallProgress / 100) * 360}deg` }]
                }
              ]} />
              <View style={styles.progressRingInner}>
                <Ionicons name="trending-up" size={32} color="#FFFFFF" />
              </View>
            </View>
          </View>
        </LinearGradient>
      </View>
    );
  };

  const renderProgressCard = (category: ProgressCategory) => (
    <TouchableOpacity key={category.id} style={styles.progressCard}>
      <Image 
        source={{ uri: category.imageUrl }} 
        style={styles.progressCardImage}
        resizeMode="cover"
      />
      <LinearGradient
        colors={['transparent', 'rgba(0,0,0,0.8)']}
        style={styles.progressCardOverlay}
      >
        <View style={styles.progressCardContent}>
          <View style={styles.progressCardHeader}>
            <View style={styles.progressCardInfo}>
              <Ionicons name={category.icon as any} size={24} color="#FFFFFF" />
              <Text style={styles.progressCardTitle}>{category.title}</Text>
            </View>
            <View style={styles.trendIndicator}>
              <Ionicons 
                name={category.trend === 'up' ? 'trending-up' : 
                     category.trend === 'down' ? 'trending-down' : 'remove'} 
                size={16} 
                color={category.trend === 'up' ? '#4CAF50' : 
                       category.trend === 'down' ? '#FF4444' : '#FFA500'} 
              />
              <Text style={[
                styles.trendText,
                { color: category.trend === 'up' ? '#4CAF50' : 
                         category.trend === 'down' ? '#FF4444' : '#FFA500' }
              ]}>
                {category.change > 0 ? '+' : ''}{category.change}%
              </Text>
            </View>
          </View>

          <View style={styles.progressInfo}>
            <Text style={styles.progressValue}>
              {category.progress}{category.unit}
            </Text>
            <Text style={styles.progressTarget}>
              of {category.target}{category.unit}
            </Text>
          </View>

          <View style={styles.progressBarContainer}>
            <View style={styles.progressBar}>
              <LinearGradient
                colors={category.color}
                style={[
                  styles.progressBarFill,
                  { width: `${(category.progress / category.target) * 100}%` }
                ]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              />
            </View>
          </View>
        </View>
      </LinearGradient>
    </TouchableOpacity>
  );

  const renderMilestones = () => (
    <View style={styles.milestonesSection}>
      <Text style={styles.sectionTitle}>Recent Milestones</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {[
          { id: '1', title: '7-Day Streak', description: 'Consistent workouts', icon: 'flame', color: '#FF6B35' },
          { id: '2', title: 'Budget Goal', description: 'Monthly savings target', icon: 'trophy', color: '#4CAF50' },
          { id: '3', title: 'Meal Prep', description: '5 healthy meals planned', icon: 'restaurant', color: '#2196F3' },
        ].map((milestone) => (
          <View key={milestone.id} style={styles.milestoneCard}>
            <View style={[styles.milestoneIcon, { backgroundColor: milestone.color }]}>
              <Ionicons name={milestone.icon as any} size={24} color="#FFFFFF" />
            </View>
            <Text style={styles.milestoneTitle}>{milestone.title}</Text>
            <Text style={styles.milestoneDescription}>{milestone.description}</Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );

  const renderInsights = () => (
    <View style={styles.insightsSection}>
      <Text style={styles.sectionTitle}>AI Insights</Text>
      <View style={styles.insightCard}>
        <LinearGradient
          colors={['#FF9800', '#FF5722']}
          style={styles.insightGradient}
        >
          <Ionicons name="bulb" size={24} color="#FFFFFF" />
          <Text style={styles.insightText}>
            Your productivity peaks on Tuesday mornings. Consider scheduling important tasks then!
          </Text>
        </LinearGradient>
      </View>
      <View style={styles.insightCard}>
        <LinearGradient
          colors={['#4CAF50', '#8BC34A']}
          style={styles.insightGradient}
        >
          <Ionicons name="fitness" size={24} color="#FFFFFF" />
          <Text style={styles.insightText}>
            You're 23% more likely to complete workouts when scheduled in the morning.
          </Text>
        </LinearGradient>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Progress</Text>
        <TouchableOpacity style={styles.exportButton}>
          <Ionicons name="share" size={24} color="#FF6B35" />
        </TouchableOpacity>
      </View>

      {renderPeriodSelector()}

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        {renderOverallProgress()}
        
        <View style={styles.progressGrid}>
          {progressCategories.map(renderProgressCard)}
        </View>

        {renderMilestones()}
        {renderInsights()}
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
  exportButton: {
    padding: 8,
  },
  periodSelector: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    margin: 16,
    borderRadius: 12,
    padding: 4,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  periodButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  selectedPeriodButton: {
    backgroundColor: '#FF6B35',
  },
  periodButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#8E8E93',
  },
  selectedPeriodButtonText: {
    color: '#FFFFFF',
  },
  scrollView: {
    flex: 1,
  },
  overallProgressCard: {
    margin: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  overallProgressGradient: {
    flexDirection: 'row',
    padding: 20,
    alignItems: 'center',
  },
  overallProgressContent: {
    flex: 1,
  },
  overallProgressTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  overallProgressValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  overallProgressSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  overallProgressChart: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  progressRing: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  progressRingFill: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    borderRadius: 40,
    backgroundColor: '#FFFFFF',
    opacity: 0.3,
  },
  progressRingInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  progressGrid: {
    paddingHorizontal: 16,
  },
  progressCard: {
    height: 200,
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  progressCardImage: {
    width: '100%',
    height: '100%',
  },
  progressCardOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: '70%',
    justifyContent: 'flex-end',
  },
  progressCardContent: {
    padding: 16,
  },
  progressCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  progressCardInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressCardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginLeft: 8,
  },
  trendIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  trendText: {
    fontSize: 12,
    fontWeight: '600',
    marginLeft: 4,
  },
  progressInfo: {
    marginBottom: 12,
  },
  progressValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  progressTarget: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.8,
  },
  progressBarContainer: {
    marginTop: 8,
  },
  progressBar: {
    height: 6,
    backgroundColor: 'rgba(255,255,255,0.3)',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 3,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginHorizontal: 16,
    marginBottom: 12,
  },
  milestonesSection: {
    marginVertical: 16,
  },
  milestoneCard: {
    width: 120,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginLeft: 16,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  milestoneIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  milestoneTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#1A1A1A',
    textAlign: 'center',
    marginBottom: 4,
  },
  milestoneDescription: {
    fontSize: 12,
    color: '#8E8E93',
    textAlign: 'center',
  },
  insightsSection: {
    margin: 16,
  },
  insightCard: {
    marginBottom: 12,
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  insightGradient: {
    flexDirection: 'row',
    padding: 16,
    alignItems: 'center',
  },
  insightText: {
    flex: 1,
    fontSize: 14,
    color: '#FFFFFF',
    marginLeft: 12,
    lineHeight: 20,
  },
});

export default ProgressScreen;