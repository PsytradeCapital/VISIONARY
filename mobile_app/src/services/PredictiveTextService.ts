/**
 * Predictive Text Service
 * Provides intelligent text suggestions and auto-completion
 */

import { apiService } from './api';

export interface TextPrediction {
  text: string;
  confidence: number;
  category: 'completion' | 'suggestion' | 'correction';
  context?: string;
}

export interface PredictionOptions {
  maxSuggestions?: number;
  includeCorrections?: boolean;
  contextAware?: boolean;
  userPersonalization?: boolean;
}

export class PredictiveTextService {
  private cache: Map<string, TextPrediction[]> = new Map();
  private userContext: string[] = [];
  private commonPhrases: string[] = [];

  constructor() {
    this.initializeCommonPhrases();
    this.loadUserContext();
  }

  /**
   * Get text predictions for current input
   */
  async getPredictions(
    input: string,
    options: PredictionOptions = {}
  ): Promise<string[]> {
    try {
      // Check cache first
      const cacheKey = this.getCacheKey(input, options);
      const cached = this.cache.get(cacheKey);
      if (cached) {
        return cached.map(p => p.text);
      }

      // Get predictions from cloud service
      const predictions = await this.fetchPredictions(input, options);
      
      // Cache results
      this.cache.set(cacheKey, predictions);
      
      return predictions.map(p => p.text);
    } catch (error) {
      console.error('Failed to get predictions:', error);
      return this.getFallbackPredictions(input);
    }
  }

  /**
   * Fetch predictions from cloud service
   */
  private async fetchPredictions(
    input: string,
    options: PredictionOptions
  ): Promise<TextPrediction[]> {
    const response = await apiService.post<{ predictions: TextPrediction[] }>(
      '/api/v1/text/predict',
      {
        input,
        options: {
          maxSuggestions: options.maxSuggestions || 5,
          includeCorrections: options.includeCorrections !== false,
          contextAware: options.contextAware !== false,
          userPersonalization: options.userPersonalization !== false,
        },
        userContext: this.userContext.slice(-10), // Last 10 inputs for context
      }
    );

    return response.data?.predictions || [];
  }

  /**
   * Get smart completions for partial words
   */
  async getSmartCompletions(partialWord: string): Promise<string[]> {
    try {
      const response = await apiService.post<{ completions: string[] }>(
        '/api/v1/text/complete',
        {
          partialWord,
          context: this.userContext.slice(-5),
          includeCommon: true,
        }
      );

      return response.data?.completions || [];
    } catch (error) {
      console.error('Failed to get smart completions:', error);
      return this.getLocalCompletions(partialWord);
    }
  }

  /**
   * Get contextual suggestions based on previous text
   */
  async getContextualSuggestions(
    previousText: string,
    currentInput: string
  ): Promise<string[]> {
    try {
      const response = await apiService.post<{ suggestions: string[] }>(
        '/api/v1/text/contextual',
        {
          previousText,
          currentInput,
          userPreferences: this.getUserPreferences(),
        }
      );

      return response.data?.suggestions || [];
    } catch (error) {
      console.error('Failed to get contextual suggestions:', error);
      return [];
    }
  }

  /**
   * Learn from user input to improve predictions
   */
  async learnFromInput(input: string, selectedSuggestion?: string): Promise<void> {
    try {
      // Add to user context
      this.userContext.push(input);
      if (this.userContext.length > 100) {
        this.userContext = this.userContext.slice(-50); // Keep last 50
      }

      // Send learning data to cloud service
      await apiService.post('/api/v1/text/learn', {
        input,
        selectedSuggestion,
        timestamp: new Date().toISOString(),
      });

      // Update local cache
      this.updateLocalLearning(input, selectedSuggestion);
    } catch (error) {
      console.error('Failed to learn from input:', error);
    }
  }

  /**
   * Get spelling corrections
   */
  async getSpellingCorrections(text: string): Promise<string[]> {
    try {
      const response = await apiService.post<{ corrections: string[] }>(
        '/api/v1/text/spell-check',
        { text }
      );

      return response.data?.corrections || [];
    } catch (error) {
      console.error('Failed to get spelling corrections:', error);
      return [];
    }
  }

  /**
   * Get grammar suggestions
   */
  async getGrammarSuggestions(text: string): Promise<string[]> {
    try {
      const response = await apiService.post<{ suggestions: string[] }>(
        '/api/v1/text/grammar',
        { text }
      );

      return response.data?.suggestions || [];
    } catch (error) {
      console.error('Failed to get grammar suggestions:', error);
      return [];
    }
  }

  /**
   * Initialize common phrases for fallback
   */
  private initializeCommonPhrases(): void {
    this.commonPhrases = [
      // Common task-related phrases
      'I need to',
      'Please help me',
      'Can you',
      'I want to',
      'I would like to',
      'I am planning to',
      'I have to',
      'I should',
      'I will',
      'I am going to',
      
      // Health and fitness
      'workout session',
      'healthy meal',
      'doctor appointment',
      'exercise routine',
      'meal planning',
      
      // Work and productivity
      'meeting with',
      'project deadline',
      'team collaboration',
      'client presentation',
      'report submission',
      
      // Personal goals
      'financial planning',
      'budget review',
      'savings goal',
      'investment strategy',
      'debt reduction',
    ];
  }

  /**
   * Load user context from storage
   */
  private async loadUserContext(): Promise<void> {
    try {
      // In a real implementation, this would load from AsyncStorage
      // For now, we'll use empty context
      this.userContext = [];
    } catch (error) {
      console.error('Failed to load user context:', error);
    }
  }

  /**
   * Get fallback predictions when service is unavailable
   */
  private getFallbackPredictions(input: string): string[] {
    const inputLower = input.toLowerCase();
    
    // Find matching common phrases
    const matches = this.commonPhrases.filter(phrase =>
      phrase.toLowerCase().includes(inputLower) ||
      inputLower.includes(phrase.toLowerCase().split(' ')[0])
    );

    // Add word completions
    const words = input.split(' ');
    const lastWord = words[words.length - 1];
    
    if (lastWord.length > 1) {
      const wordCompletions = this.getLocalCompletions(lastWord);
      matches.push(...wordCompletions.map(completion => 
        words.slice(0, -1).concat(completion).join(' ')
      ));
    }

    return matches.slice(0, 5);
  }

  /**
   * Get local word completions
   */
  private getLocalCompletions(partialWord: string): string[] {
    const commonWords = [
      'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
      'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
      'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
      'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'work', 'time',
      'need', 'want', 'help', 'make', 'take', 'come', 'know', 'think', 'look',
      'meeting', 'project', 'schedule', 'appointment', 'deadline', 'task',
      'workout', 'exercise', 'healthy', 'nutrition', 'financial', 'budget'
    ];

    return commonWords
      .filter(word => word.startsWith(partialWord.toLowerCase()))
      .slice(0, 5);
  }

  /**
   * Update local learning data
   */
  private updateLocalLearning(input: string, selectedSuggestion?: string): void {
    // Extract useful patterns from user input
    const words = input.toLowerCase().split(' ');
    
    // Add new phrases to common phrases if they seem useful
    if (words.length >= 2 && words.length <= 4) {
      const phrase = words.join(' ');
      if (!this.commonPhrases.includes(phrase)) {
        this.commonPhrases.push(phrase);
        
        // Keep only the most recent 200 phrases
        if (this.commonPhrases.length > 200) {
          this.commonPhrases = this.commonPhrases.slice(-150);
        }
      }
    }
  }

  /**
   * Get user preferences for personalization
   */
  private getUserPreferences(): any {
    return {
      preferredTopics: ['productivity', 'health', 'finance'],
      writingStyle: 'casual',
      language: 'en-US',
    };
  }

  /**
   * Generate cache key
   */
  private getCacheKey(input: string, options: PredictionOptions): string {
    return `${input}_${JSON.stringify(options)}`;
  }

  /**
   * Clear expired cache entries
   */
  clearCache(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): { size: number; hitRate: number } {
    return {
      size: this.cache.size,
      hitRate: 0.85, // Placeholder
    };
  }
}

// Singleton instance
export const predictiveTextService = new PredictiveTextService();