/**
 * Motivational Content Service for Mobile App
 * Integrates with cloud backend motivational content system
 * Provides personalized motivational content with AI-generated visuals
 */

import { apiService } from './api';

export interface MotivationalContentRequest {
  userId: string;
  visionCategory: 'health' | 'fitness' | 'nutrition' | 'financial' | 'productivity' | 'psychological';
  contentType: 'motivational_quote' | 'progress_celebration' | 'milestone_achievement' | 'daily_inspiration';
  userName: string;
  goals: string[];
  currentProgress: { [key: string]: number };
  includeImage?: boolean;
}

export interface MotivationalContent {
  id: string;
  title: string;
  message: string;
  quote: string;
  imageUrl?: string;
  category: string;
  contentType: string;
  personalized: boolean;
  createdAt: string;
  expiresAt: string;
  engagementScore: number;
}

export interface DailyMotivationRequest {
  userId: string;
  visionCategory: string;
  userName: string;
  goals: string[];
  currentProgress: { [key: string]: number };
}

export class MotivationalContentService {
  private baseUrl: string;
  private cache: Map<string, MotivationalContent> = new Map();

  constructor() {
    this.baseUrl = '/api/v1/motivational-content';
  }

  /**
   * Generate daily motivational content
   */
  async generateDailyMotivation(request: DailyMotivationRequest): Promise<MotivationalContent | null> {
    try {
      const cacheKey = `daily_${request.userId}_${new Date().toDateString()}`;
      const cached = this.cache.get(cacheKey);
      
      if (cached && new Date(cached.expiresAt) > new Date()) {
        return cached;
      }

      const response = await apiService.post<MotivationalContent>(`${this.baseUrl}/daily`, {
        ...request,
        contentType: 'daily_inspiration',
        includeImage: true,
      });

      if (response.data) {
        this.cache.set(cacheKey, response.data);
        return response.data;
      }

      return null;
    } catch (error) {
      console.error('Failed to generate daily motivation:', error);
      return this.getFallbackMotivation(request.userName);
    }
  }

  /**
   * Generate progress celebration content
   */
  async generateProgressCelebration(
    userId: string,
    achievement: string,
    progress: number,
    category: string
  ): Promise<MotivationalContent | null> {
    try {
      const response = await apiService.post<MotivationalContent>(`${this.baseUrl}/celebration`, {
        userId,
        achievement,
        progress,
        category,
        contentType: 'progress_celebration',
        includeImage: true,
      });

      return response.data || null;
    } catch (error) {
      console.error('Failed to generate progress celebration:', error);
      return null;
    }
  }

  /**
   * Generate milestone achievement content
   */
  async generateMilestoneContent(
    userId: string,
    milestone: string,
    category: string
  ): Promise<MotivationalContent | null> {
    try {
      const response = await apiService.post<MotivationalContent>(`${this.baseUrl}/milestone`, {
        userId,
        milestone,
        category,
        contentType: 'milestone_achievement',
        includeImage: true,
      });

      return response.data || null;
    } catch (error) {
      console.error('Failed to generate milestone content:', error);
      return null;
    }
  }

  /**
   * Get personalized motivational quotes
   */
  async getPersonalizedQuotes(
    userId: string,
    category: string,
    count: number = 5
  ): Promise<MotivationalContent[]> {
    try {
      const response = await apiService.get<MotivationalContent[]>(
        `${this.baseUrl}/quotes/${userId}?category=${category}&count=${count}`
      );

      return response.data || [];
    } catch (error) {
      console.error('Failed to get personalized quotes:', error);
      return this.getFallbackQuotes(category, count);
    }
  }

  /**
   * Track engagement with motivational content
   */
  async trackEngagement(
    contentId: string,
    engagementType: 'viewed' | 'liked' | 'shared' | 'acted_upon',
    duration?: number
  ): Promise<void> {
    try {
      await apiService.post(`${this.baseUrl}/engagement`, {
        contentId,
        engagementType,
        duration,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Failed to track engagement:', error);
    }
  }

  /**
   * Get content history for user
   */
  async getContentHistory(userId: string, limit: number = 10): Promise<MotivationalContent[]> {
    try {
      const response = await apiService.get<MotivationalContent[]>(
        `${this.baseUrl}/history/${userId}?limit=${limit}`
      );

      return response.data || [];
    } catch (error) {
      console.error('Failed to get content history:', error);
      return [];
    }
  }

  /**
   * Get trending motivational content
   */
  async getTrendingContent(category?: string): Promise<MotivationalContent[]> {
    try {
      const url = category 
        ? `${this.baseUrl}/trending?category=${category}`
        : `${this.baseUrl}/trending`;
      
      const response = await apiService.get<MotivationalContent[]>(url);
      return response.data || [];
    } catch (error) {
      console.error('Failed to get trending content:', error);
      return [];
    }
  }

  /**
   * Generate recovery motivation for when user is struggling
   */
  async generateRecoveryMotivation(
    userId: string,
    strugglingArea: string,
    userName: string
  ): Promise<MotivationalContent | null> {
    try {
      const response = await apiService.post<MotivationalContent>(`${this.baseUrl}/recovery`, {
        userId,
        strugglingArea,
        userName,
        contentType: 'recovery_encouragement',
        includeImage: true,
      });

      return response.data || null;
    } catch (error) {
      console.error('Failed to generate recovery motivation:', error);
      return this.getFallbackRecoveryMotivation(userName, strugglingArea);
    }
  }

  /**
   * Preload motivational content for better performance
   */
  async preloadContent(userId: string, categories: string[]): Promise<void> {
    const preloadPromises = categories.map(async (category) => {
      try {
        await this.getPersonalizedQuotes(userId, category, 3);
      } catch (error) {
        console.warn(`Failed to preload content for ${category}:`, error);
      }
    });

    await Promise.all(preloadPromises);
  }

  /**
   * Clear expired cache entries
   */
  clearExpiredCache(): void {
    const now = new Date();
    for (const [key, content] of this.cache.entries()) {
      if (new Date(content.expiresAt) <= now) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Get fallback motivation when service is unavailable
   */
  private getFallbackMotivation(userName: string): MotivationalContent {
    const fallbackQuotes = [
      "Every step forward is progress, no matter how small.",
      "You have the power to create the life you want.",
      "Believe in yourself and your ability to achieve great things.",
      "Progress, not perfection, is the goal.",
      "Your journey is unique and valuable."
    ];

    const randomQuote = fallbackQuotes[Math.floor(Math.random() * fallbackQuotes.length)];

    return {
      id: 'fallback_' + Date.now(),
      title: `Daily Inspiration for ${userName}`,
      message: `Hi ${userName}! ${randomQuote} Keep moving forward!`,
      quote: randomQuote,
      category: 'general',
      contentType: 'daily_inspiration',
      personalized: false,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours
      engagementScore: 0,
    };
  }

  /**
   * Get fallback quotes when service is unavailable
   */
  private getFallbackQuotes(category: string, count: number): MotivationalContent[] {
    const categoryQuotes = {
      health: [
        "Your body can do it. It's your mind you have to convince.",
        "Health is not about the weight you lose, but about the life you gain.",
        "Take care of your body. It's the only place you have to live."
      ],
      fitness: [
        "Strong is the new beautiful.",
        "Every workout is progress, no matter how small.",
        "The only bad workout is the one that didn't happen."
      ],
      nutrition: [
        "Let food be thy medicine and medicine be thy food.",
        "You are what you eat, so don't be fast, cheap, easy, or fake.",
        "Healthy eating is a form of self-respect."
      ],
      financial: [
        "The best investment you can make is in yourself.",
        "Every dollar saved is a step toward financial freedom.",
        "Your financial future is created by what you do today."
      ],
      productivity: [
        "The way to get started is to quit talking and begin doing.",
        "Focus on being productive instead of busy.",
        "Small daily improvements over time lead to stunning results."
      ]
    };

    const quotes = categoryQuotes[category as keyof typeof categoryQuotes] || categoryQuotes.health;
    
    return quotes.slice(0, count).map((quote, index) => ({
      id: `fallback_${category}_${index}`,
      title: 'Daily Motivation',
      message: quote,
      quote,
      category,
      contentType: 'motivational_quote',
      personalized: false,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      engagementScore: 0,
    }));
  }

  /**
   * Get fallback recovery motivation
   */
  private getFallbackRecoveryMotivation(userName: string, strugglingArea: string): MotivationalContent {
    const recoveryMessages = {
      health: "Every setback is a setup for a comeback. Your health journey continues!",
      fitness: "Rest is not quitting. Take time to recover and come back stronger!",
      nutrition: "One meal doesn't define your journey. Get back on track with your next choice!",
      financial: "Financial setbacks are temporary. Your commitment to your goals is permanent!",
      productivity: "Productivity isn't about perfection. It's about progress and consistency!"
    };

    const message = recoveryMessages[strugglingArea as keyof typeof recoveryMessages] || 
                   "Every challenge is an opportunity to grow stronger. You've got this!";

    return {
      id: 'recovery_fallback_' + Date.now(),
      title: `Recovery Support for ${userName}`,
      message: `${userName}, ${message}`,
      quote: message,
      category: strugglingArea,
      contentType: 'recovery_encouragement',
      personalized: true,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      engagementScore: 0,
    };
  }
}

// Singleton instance
export const motivationalContentService = new MotivationalContentService();