/**
 * AI Image Service for Photorealistic Image Generation
 * Integrates with cloud backend AI Visual Generator Service
 * Ensures all images are professional photography quality
 */

import { apiService } from './api';

export interface AIImageRequest {
  category: 'health' | 'nutrition' | 'financial' | 'productivity' | 'wellness';
  style: 'real_people_exercising' | 'healthy_food_photography' | 'success_environments' | 'achievement_celebrations' | 'peaceful_wellness';
  context: string;
  quality: 'hd' | 'standard';
  size?: '1024x1024' | '1792x1024' | '1024x1792';
}

export interface AIImageResponse {
  id: string;
  url: string;
  category: string;
  style: string;
  quality: string;
  isPhotorealistic: boolean;
  generatedAt: string;
  expiresAt: string;
}

export interface ImageQualityValidation {
  isPhotorealistic: boolean;
  qualityScore: number;
  hasRealPeople: boolean;
  hasRealEnvironments: boolean;
  rejectionReasons: string[];
}

export class AIImageService {
  private baseUrl: string;
  private cache: Map<string, AIImageResponse> = new Map();
  private qualityThreshold = 0.8; // Minimum quality score for acceptance

  constructor() {
    this.baseUrl = '/api/v1/ai-images';
  }

  /**
   * Generate photorealistic AI image with quality validation
   */
  async generatePhotorealisticImage(request: AIImageRequest): Promise<AIImageResponse | null> {
    try {
      // Check cache first
      const cacheKey = this.getCacheKey(request);
      const cached = this.cache.get(cacheKey);
      if (cached && new Date(cached.expiresAt) > new Date()) {
        return cached;
      }

      // Generate image via cloud backend
      const response = await apiService.post<AIImageResponse>(`${this.baseUrl}/generate`, {
        ...request,
        enforcePhotorealistic: true,
        qualityValidation: true,
      });

      if (response.data) {
        // Validate image quality
        const validation = await this.validateImageQuality(response.data.url);
        
        if (!validation.isPhotorealistic || validation.qualityScore < this.qualityThreshold) {
          console.warn('Generated image failed quality validation:', validation.rejectionReasons);
          
          // Retry with enhanced prompt
          const enhancedRequest = this.enhancePromptForPhotorealism(request);
          const retryResponse = await apiService.post<AIImageResponse>(`${this.baseUrl}/generate`, {
            ...enhancedRequest,
            enforcePhotorealistic: true,
            qualityValidation: true,
            retry: true,
          });

          if (retryResponse.data) {
            const retryValidation = await this.validateImageQuality(retryResponse.data.url);
            if (retryValidation.isPhotorealistic && retryValidation.qualityScore >= this.qualityThreshold) {
              this.cache.set(cacheKey, retryResponse.data);
              return retryResponse.data;
            }
          }
          
          return null; // Failed to generate acceptable image
        }

        // Cache successful result
        this.cache.set(cacheKey, response.data);
        return response.data;
      }

      return null;
    } catch (error) {
      console.error('Failed to generate AI image:', error);
      return null;
    }
  }

  /**
   * Validate image quality to ensure photorealistic standards
   */
  private async validateImageQuality(imageUrl: string): Promise<ImageQualityValidation> {
    try {
      const response = await apiService.post<ImageQualityValidation>(`${this.baseUrl}/validate-quality`, {
        imageUrl,
        criteria: {
          requirePhotorealistic: true,
          requireRealPeople: true,
          requireRealEnvironments: true,
          minQualityScore: this.qualityThreshold,
        }
      });

      return response.data || {
        isPhotorealistic: false,
        qualityScore: 0,
        hasRealPeople: false,
        hasRealEnvironments: false,
        rejectionReasons: ['Validation failed']
      };
    } catch (error) {
      console.error('Image quality validation failed:', error);
      return {
        isPhotorealistic: false,
        qualityScore: 0,
        hasRealPeople: false,
        hasRealEnvironments: false,
        rejectionReasons: ['Validation service unavailable']
      };
    }
  }

  /**
   * Enhance prompt to improve photorealistic quality
   */
  private enhancePromptForPhotorealism(request: AIImageRequest): AIImageRequest {
    const photorealisticEnhancements = {
      health: 'professional photography of real people, natural lighting, high resolution, authentic gym environment, real fitness equipment',
      nutrition: 'professional food photography, natural lighting, real fresh ingredients, high quality, appetizing presentation, real kitchen setting',
      financial: 'professional business photography, real office environment, authentic business setting, natural lighting, real people in professional attire',
      productivity: 'professional workplace photography, real office space, authentic work environment, natural lighting, real people working',
      wellness: 'professional lifestyle photography, real people in natural settings, authentic wellness environment, natural lighting'
    };

    const enhancement = photorealisticEnhancements[request.category] || 'professional photography, natural lighting, high quality, photorealistic';

    return {
      ...request,
      context: `${request.context}, ${enhancement}, no cartoon or illustration style, no digital art, no graphics`,
      quality: 'hd' as const,
    };
  }

  /**
   * Get cached images for a category
   */
  async getCachedImages(category: string): Promise<AIImageResponse[]> {
    const cached = Array.from(this.cache.values()).filter(
      image => image.category === category && new Date(image.expiresAt) > new Date()
    );

    if (cached.length > 0) {
      return cached;
    }

    // Fetch from backend if no cache
    try {
      const response = await apiService.get<AIImageResponse[]>(`${this.baseUrl}/category/${category}`);
      return response.data || [];
    } catch (error) {
      console.error('Failed to fetch cached images:', error);
      return [];
    }
  }

  /**
   * Preload images for better performance
   */
  async preloadImages(categories: string[]): Promise<void> {
    const preloadPromises = categories.map(async (category) => {
      const requests: AIImageRequest[] = [
        {
          category: category as any,
          style: 'real_people_exercising',
          context: `${category} motivation with real people`,
          quality: 'hd'
        }
      ];

      for (const request of requests) {
        try {
          await this.generatePhotorealisticImage(request);
        } catch (error) {
          console.warn(`Failed to preload image for ${category}:`, error);
        }
      }
    });

    await Promise.all(preloadPromises);
  }

  /**
   * Clear expired cache entries
   */
  clearExpiredCache(): void {
    const now = new Date();
    for (const [key, image] of this.cache.entries()) {
      if (new Date(image.expiresAt) <= now) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Get fallback placeholder images
   */
  getFallbackImage(category: string): string {
    const fallbacks = {
      health: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop&crop=center',
      nutrition: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&h=300&fit=crop&crop=center',
      financial: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop&crop=center',
      productivity: 'https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?w=400&h=300&fit=crop&crop=center',
      wellness: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop&crop=center'
    };

    return fallbacks[category as keyof typeof fallbacks] || fallbacks.health;
  }

  private getCacheKey(request: AIImageRequest): string {
    return `${request.category}_${request.style}_${request.quality}_${request.context.slice(0, 50)}`;
  }
}

// Singleton instance
export const aiImageService = new AIImageService();