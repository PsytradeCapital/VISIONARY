/**
 * Main Mobile Dashboard with Photorealistic AI-Generated Visuals
 * Task 10.1: Create main mobile dashboard with photorealistic AI-generated visuals
 * 
 * Features:
 * - Mobile-first schedule display with touch-friendly navigation
 * - Premium visual elements with photorealistic AI-generated images
 * - Real people in health scenarios, real food for nutrition, real success environments
 * - Professional photography quality validation
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Image,
  RefreshControl,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useDispatch, useSelector } from 'react-redux';

import { RootState } from '../store/store';
import { fetchSchedule } from '../store/slices/scheduleSlice';
import { fetchAnalytics } from '../store/slices/analyticsSlice';
import { AIImageService } from '../services/AIImageService';
import { MotivationalContentService } from '../services/MotivationalContentService';

const { width, height } = Dimensions.get('window');

interface DashboardCard {
  id: string;
  title: string;
  subtitle: string;
  imageUrl?: string;
  progress?: number;
  type: 'schedule' | 'progress' | 'motivation' | 'health' | 'financial';
  onPress: () => void;
}

const DashboardScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { todaySchedule, loading: scheduleLoading } = useSelector((state: RootState) => state.schedule);
  const { analytics, loading: analyticsLoading } = useSelector((state: RootState) => state.analytics);
  
  const [refreshing, setRefreshing] = useState(false);
  const [dashboardCards, setDashboardCards] = useState<DashboardCard[]>([]);
  const [motivationalContent, setMotivationalContent] = useState<any>(null);
  const [aiImages, setAiImages] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    loadDashboardData();
    generateMotivationalContent();
    loadAIGeneratedImages();
  }, []);

  const loadDashboardData = async () => {
    try {
      // @ts-ignore - dispatch returns a promise in RTK
      await dispatch(fetchSchedule());
      // @ts-ignore
      await dispatch(fetchAnalytics());
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const generateMotivationalContent = async () => {
    try {
      const contentService = new MotivationalContentService();
      const content = await contentService.generateDailyMotivation({
        userId: user?.id || 'demo_user',
        visionCategory: 'health', // This would come from user preferences
        userName: user?.name || 'Champion',
        goals: ['fitness', 'nutrition', 'productivity'],
        currentProgress: analytics?.progressSummary || {}
      });
      
      setMotivationalContent(content);
    } catch (error) {
      console.error('Failed to generate motivational content:', error);
    }
  };

  const loadAIGeneratedImages = async () => {
    try {
      const imageService = new AIImageService();
      
      // Generate photorealistic images for different categories
      const imagePromises = [
        imageService.generatePhotorealisticImage({
          category: 'health',
          style: 'real_people_exercising',
          context: 'diverse group of real people doing morning yoga in bright studio',
          quality: 'hd'
        }),
        imageService.generatePhotorealisticImage({
          category: 'nutrition',
          style: 'healthy_food_photography',
          context: 'colorful array of fresh fruits and vegetables, professional food photography',
          quality: 'hd'
        }),
        imageService.generatePhotorealisticImage({
          category: 'financial',
          style: 'success_environments',
          context: 'successful real person in modern office, confident professional achievement',
          quality: 'hd'
        }),
        imageService.generatePhotorealisticImage({
          category: 'productivity',
          style: 'achievement_celebrations',
          context: 'real person celebrating work milestone, genuine joy and accomplishment',
          quality: 'hd'
        })
      ];

      const images = await Promise.all(imagePromises);
      
      setAiImages({
        health: images[0]?.url || '',
        nutrition: images[1]?.url || '',
        financial: images[2]?.url || '',
        productivity: images[3]?.url || ''
      });
    } catch (error) {
      console.error('Failed to load AI-generated images:', error);
      // Fallback to placeholder images
      setAiImages({
        health: 'https://via.placeholder.com/300x200/FF6B35/FFFFFF?text=Health+Goals',
        nutrition: 'https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=Nutrition',
        financial: 'https://via.placeholder.com/300x200/2196F3/FFFFFF?text=Financial',
        productivity: 'https://via.placeholder.com/300x200/9C27B0/FFFFFF?text=Productivity'
      });
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    await generateMotivationalContent();
    setRefreshing(false);
  };

  const handleCardPress = (type: string) => {
    switch (type) {
      case 'schedule':
        // Navigate to schedule screen
        break;
      case 'progress':
        // Navigate to progress screen
        break;
      case 'upload':
        // Navigate to upload screen
        break;
      default:
        Alert.alert('Coming Soon', 'This feature is being developed!');
    }
  };

  const renderWelcomeSection = () => (
    <LinearGradient
      colors={['#FF6B35', '#F7931E']}
      style={styles.welcomeSection}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
    >
      <View style={styles.welcomeContent}>
        <Text style={styles.welcomeText}>
          Good {getTimeOfDay()}, {user?.name || 'Champion'}!
        </Text>
        <Text style={styles.welcomeSubtext}>
          Ready to make today amazing?
        </Text>
      </View>
      <View style={styles.welcomeStats}>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{analytics?.todayTasks || 0}</Text>
          <Text style={styles.statLabel}>Tasks Today</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{analytics?.completionRate || 0}%</Text>
          <Text style={styles.statLabel}>Complete</Text>
        </View>
      </View>
    </LinearGradient>
  );

  const renderMotivationalCard = () => {
    if (!motivationalContent) return null;

    return (
      <TouchableOpacity style={styles.motivationalCard} onPress={() => handleCardPress('motivation')}>
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.motivationalGradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.motivationalContent}>
            <Ionicons name="star" size={24} color="#FFFFFF" />
            <Text style={styles.motivationalTitle}>{motivationalContent.title}</Text>
            <Text style={styles.motivationalMessage} numberOfLines={3}>
              {motivationalContent.message}
            </Text>
          </View>
          {motivationalContent.imageUrl && (
            <Image 
              source={{ uri: motivationalContent.imageUrl }} 
              style={styles.motivationalImage}
              resizeMode="cover"
            />
          )}
        </LinearGradient>
      </TouchableOpacity>
    );
  };

  const renderProgressCards = () => (
    <View style={styles.progressSection}>
      <Text style={styles.sectionTitle}>Your Progress</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.progressScroll}>
        {/* Health Progress Card */}
        <TouchableOpacity style={styles.progressCard} onPress={() => handleCardPress('health')}>
          <Image 
            source={{ uri: aiImages.health }} 
            style={styles.progressCardImage}
            resizeMode="cover"
          />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.7)']}
            style={styles.progressCardOverlay}
          >
            <View style={styles.progressCardContent}>
              <Text style={styles.progressCardTitle}>Health Goals</Text>
              <Text style={styles.progressCardSubtitle}>
                {analytics?.healthProgress || 0}% Complete
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressBarFill, 
                    { width: `${analytics?.healthProgress || 0}%` }
                  ]} 
                />
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* Nutrition Progress Card */}
        <TouchableOpacity style={styles.progressCard} onPress={() => handleCardPress('nutrition')}>
          <Image 
            source={{ uri: aiImages.nutrition }} 
            style={styles.progressCardImage}
            resizeMode="cover"
          />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.7)']}
            style={styles.progressCardOverlay}
          >
            <View style={styles.progressCardContent}>
              <Text style={styles.progressCardTitle}>Nutrition</Text>
              <Text style={styles.progressCardSubtitle}>
                {analytics?.nutritionProgress || 0}% Complete
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressBarFill, 
                    { width: `${analytics?.nutritionProgress || 0}%` }
                  ]} 
                />
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>

        {/* Financial Progress Card */}
        <TouchableOpacity style={styles.progressCard} onPress={() => handleCardPress('financial')}>
          <Image 
            source={{ uri: aiImages.financial }} 
            style={styles.progressCardImage}
            resizeMode="cover"
          />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.7)']}
            style={styles.progressCardOverlay}
          >
            <View style={styles.progressCardContent}>
              <Text style={styles.progressCardTitle}>Financial Goals</Text>
              <Text style={styles.progressCardSubtitle}>
                {analytics?.financialProgress || 0}% Complete
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressBarFill, 
                    { width: `${analytics?.financialProgress || 0}%` }
                  ]} 
                />
              </View>
            </View>
          </LinearGradient>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );

  const renderQuickActions = () => (
    <View style={styles.quickActionsSection}>
      <Text style={styles.sectionTitle}>Quick Actions</Text>
      <View style={styles.quickActionsGrid}>
        <TouchableOpacity style={styles.quickActionCard} onPress={() => handleCardPress('schedule')}>
          <LinearGradient
            colors={['#4CAF50', '#8BC34A']}
            style={styles.quickActionGradient}
          >
            <Ionicons name="calendar" size={32} color="#FFFFFF" />
            <Text style={styles.quickActionText}>View Schedule</Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionCard} onPress={() => handleCardPress('upload')}>
          <LinearGradient
            colors={['#2196F3', '#03DAC6']}
            style={styles.quickActionGradient}
          >
            <Ionicons name="cloud-upload" size={32} color="#FFFFFF" />
            <Text style={styles.quickActionText}>Upload Content</Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionCard} onPress={() => handleCardPress('progress')}>
          <LinearGradient
            colors={['#9C27B0', '#E91E63']}
            style={styles.quickActionGradient}
          >
            <Ionicons name="analytics" size={32} color="#FFFFFF" />
            <Text style={styles.quickActionText}>View Progress</Text>
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity style={styles.quickActionCard} onPress={() => handleCardPress('ai')}>
          <LinearGradient
            colors={['#FF9800', '#FF5722']}
            style={styles.quickActionGradient}
          >
            <Ionicons name="sparkles" size={32} color="#FFFFFF" />
            <Text style={styles.quickActionText}>AI Insights</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );

  const getTimeOfDay = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Morning';
    if (hour < 17) return 'Afternoon';
    return 'Evening';
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        {renderWelcomeSection()}
        {renderMotivationalCard()}
        {renderProgressCards()}
        {renderQuickActions()}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollView: {
    flex: 1,
  },
  welcomeSection: {
    margin: 16,
    borderRadius: 16,
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  welcomeContent: {
    flex: 1,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  welcomeSubtext: {
    fontSize: 16,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  welcomeStats: {
    alignItems: 'center',
  },
  statItem: {
    alignItems: 'center',
    marginVertical: 4,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  statLabel: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.8,
  },
  motivationalCard: {
    margin: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  motivationalGradient: {
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
  },
  motivationalContent: {
    flex: 1,
  },
  motivationalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginVertical: 8,
  },
  motivationalMessage: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    lineHeight: 20,
  },
  motivationalImage: {
    width: 80,
    height: 80,
    borderRadius: 12,
    marginLeft: 16,
  },
  progressSection: {
    marginVertical: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginHorizontal: 16,
    marginBottom: 12,
  },
  progressScroll: {
    paddingLeft: 16,
  },
  progressCard: {
    width: width * 0.7,
    height: 200,
    marginRight: 16,
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
    height: '60%',
    justifyContent: 'flex-end',
  },
  progressCardContent: {
    padding: 16,
  },
  progressCardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  progressCardSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    marginBottom: 8,
  },
  progressBar: {
    height: 4,
    backgroundColor: 'rgba(255,255,255,0.3)',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 2,
  },
  quickActionsSection: {
    margin: 16,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickActionCard: {
    width: (width - 48) / 2,
    marginBottom: 16,
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  quickActionGradient: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 100,
  },
  quickActionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
    marginTop: 8,
    textAlign: 'center',
  },
});

export default DashboardScreen;