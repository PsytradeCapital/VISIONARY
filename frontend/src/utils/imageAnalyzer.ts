interface ImageMetadata {
  id: string;
  src: string;
  title: string;
  category: string;
  rating: number;
  useCase: string[];
  colors: string[];
  designStyle: string;
  complexity: 'simple' | 'moderate' | 'complex';
  accessibility: number; // 1-5 score
  mobileOptimized: boolean;
}

export class ImageAnalyzer {
  private images: ImageMetadata[] = [
    {
      id: 'image1',
      src: '/images/image1.jfif.jpeg',
      title: 'AI Dashboard Concept',
      category: 'Dashboard',
      rating: 4.5,
      useCase: ['dashboard', 'main-interface', 'overview'],
      colors: ['blue', 'white', 'gray'],
      designStyle: 'modern',
      complexity: 'moderate',
      accessibility: 4,
      mobileOptimized: true
    },
    {
      id: 'image2',
      src: '/images/image2.jpeg',
      title: 'Schedule Planning',
      category: 'Scheduling',
      rating: 4.8,
      useCase: ['scheduling', 'calendar', 'planning'],
      colors: ['green', 'white', 'blue'],
      designStyle: 'clean',
      complexity: 'simple',
      accessibility: 5,
      mobileOptimized: true
    },
    {
      id: 'image3',
      src: '/images/image3.jpeg',
      title: 'Progress Tracking',
      category: 'Analytics',
      rating: 4.6,
      useCase: ['progress', 'analytics', 'charts'],
      colors: ['orange', 'blue', 'white'],
      designStyle: 'data-focused',
      complexity: 'moderate',
      accessibility: 4,
      mobileOptimized: false
    },
    {
      id: 'image4',
      src: '/images/image4.jpeg',
      title: 'Personal Assistant',
      category: 'AI Assistant',
      rating: 4.7,
      useCase: ['ai-chat', 'assistant', 'interaction'],
      colors: ['purple', 'white', 'blue'],
      designStyle: 'conversational',
      complexity: 'simple',
      accessibility: 5,
      mobileOptimized: true
    },
    {
      id: 'image7',
      src: '/images/image7.jpeg',
      title: 'Data Visualization',
      category: 'Analytics',
      rating: 4.4,
      useCase: ['data-viz', 'charts', 'insights'],
      colors: ['multi-color', 'dark', 'bright'],
      designStyle: 'complex-data',
      complexity: 'complex',
      accessibility: 3,
      mobileOptimized: false
    },
    {
      id: 'image8',
      src: '/images/image8.jpeg',
      title: 'Mobile Interface',
      category: 'Mobile',
      rating: 4.3,
      useCase: ['mobile', 'responsive', 'touch'],
      colors: ['clean', 'minimal', 'white'],
      designStyle: 'minimal',
      complexity: 'simple',
      accessibility: 5,
      mobileOptimized: true
    },
    {
      id: 'image9',
      src: '/images/image9.jpeg',
      title: 'Calendar Integration',
      category: 'Calendar',
      rating: 4.5,
      useCase: ['calendar', 'scheduling', 'time-management'],
      colors: ['blue', 'white', 'accent'],
      designStyle: 'functional',
      complexity: 'moderate',
      accessibility: 4,
      mobileOptimized: true
    },
    {
      id: 'image10',
      src: '/images/image10.jpeg',
      title: 'Goal Setting',
      category: 'Goals',
      rating: 4.6,
      useCase: ['goals', 'targets', 'motivation'],
      colors: ['green', 'success', 'growth'],
      designStyle: 'motivational',
      complexity: 'simple',
      accessibility: 4,
      mobileOptimized: true
    }
  ];

  // Get best images by rating
  getBestRated(count: number = 5): ImageMetadata[] {
    return [...this.images]
      .sort((a, b) => b.rating - a.rating)
      .slice(0, count);
  }

  // Get images by category
  getByCategory(category: string): ImageMetadata[] {
    return this.images.filter(img => img.category === category);
  }

  // Get images by use case
  getByUseCase(useCase: string): ImageMetadata[] {
    return this.images.filter(img => img.useCase.includes(useCase));
  }

  // Get mobile-optimized images
  getMobileOptimized(): ImageMetadata[] {
    return this.images.filter(img => img.mobileOptimized);
  }

  // Get high accessibility images
  getHighAccessibility(minScore: number = 4): ImageMetadata[] {
    return this.images.filter(img => img.accessibility >= minScore);
  }

  // Analyze color compatibility
  analyzeColorCompatibility(imageIds: string[]): {
    compatible: boolean;
    dominantColors: string[];
    recommendation: string;
  } {
    const selectedImages = this.images.filter(img => imageIds.includes(img.id));
    const allColors = selectedImages.flatMap(img => img.colors);
    const colorCounts = allColors.reduce((acc, color) => {
      acc[color] = (acc[color] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const dominantColors = Object.entries(colorCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([color]) => color);

    const hasConflictingColors = allColors.includes('dark') && allColors.includes('white');
    const compatible = !hasConflictingColors || dominantColors.includes('blue');

    return {
      compatible,
      dominantColors,
      recommendation: compatible 
        ? 'Colors work well together for a cohesive design'
        : 'Consider adjusting color schemes for better harmony'
    };
  }

  // Get recommended blend for specific purpose
  getRecommendedBlend(purpose: 'dashboard' | 'mobile' | 'analytics' | 'complete'): {
    images: ImageMetadata[];
    reasoning: string;
    score: number;
  } {
    let selectedImages: ImageMetadata[] = [];
    let reasoning = '';

    switch (purpose) {
      case 'dashboard':
        selectedImages = [
          ...this.getByUseCase('dashboard').slice(0, 1),
          ...this.getByUseCase('overview').slice(0, 1),
          ...this.getBestRated(2).filter(img => img.complexity !== 'complex')
        ];
        reasoning = 'Selected images focus on clean dashboard design with good usability';
        break;

      case 'mobile':
        selectedImages = this.getMobileOptimized()
          .filter(img => img.complexity === 'simple')
          .slice(0, 4);
        reasoning = 'Prioritized mobile-optimized, simple designs for touch interfaces';
        break;

      case 'analytics':
        selectedImages = [
          ...this.getByCategory('Analytics'),
          ...this.getByUseCase('charts').slice(0, 2)
        ];
        reasoning = 'Focused on data visualization and analytics capabilities';
        break;

      case 'complete':
        selectedImages = [
          this.getBestRated(1)[0], // Best overall
          ...this.getByCategory('Dashboard').slice(0, 1),
          ...this.getByCategory('Analytics').slice(0, 1),
          ...this.getMobileOptimized().slice(0, 1)
        ];
        reasoning = 'Balanced selection covering all major use cases with top-rated images';
        break;
    }

    // Remove duplicates
    selectedImages = selectedImages.filter((img, index, self) => 
      index === self.findIndex(i => i.id === img.id)
    );

    const avgRating = selectedImages.reduce((sum, img) => sum + img.rating, 0) / selectedImages.length;
    const accessibilityScore = selectedImages.reduce((sum, img) => sum + img.accessibility, 0) / selectedImages.length;
    const mobileOptimizedCount = selectedImages.filter(img => img.mobileOptimized).length;
    
    const score = (avgRating * 0.4) + (accessibilityScore * 0.3) + (mobileOptimizedCount / selectedImages.length * 0.3);

    return {
      images: selectedImages,
      reasoning,
      score: Math.round(score * 20) / 20 // Round to nearest 0.05
    };
  }

  // Analyze selection quality
  analyzeSelection(imageIds: string[]): {
    overallScore: number;
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  } {
    const selectedImages = this.images.filter(img => imageIds.includes(img.id));
    
    if (selectedImages.length === 0) {
      return {
        overallScore: 0,
        strengths: [],
        weaknesses: ['No images selected'],
        recommendations: ['Select at least 2-3 images for analysis']
      };
    }

    const avgRating = selectedImages.reduce((sum, img) => sum + img.rating, 0) / selectedImages.length;
    const avgAccessibility = selectedImages.reduce((sum, img) => sum + img.accessibility, 0) / selectedImages.length;
    const mobileOptimizedPercent = selectedImages.filter(img => img.mobileOptimized).length / selectedImages.length;
    const categoryDiversity = new Set(selectedImages.map(img => img.category)).size;
    const complexityBalance = selectedImages.filter(img => img.complexity === 'simple').length / selectedImages.length;

    const overallScore = (
      avgRating * 0.25 +
      avgAccessibility * 0.25 +
      mobileOptimizedPercent * 5 * 0.2 +
      Math.min(categoryDiversity / 3, 1) * 5 * 0.15 +
      complexityBalance * 5 * 0.15
    );

    const strengths: string[] = [];
    const weaknesses: string[] = [];
    const recommendations: string[] = [];

    if (avgRating >= 4.5) strengths.push('High-rated images selected');
    else if (avgRating < 4.0) weaknesses.push('Some low-rated images included');

    if (avgAccessibility >= 4.5) strengths.push('Excellent accessibility scores');
    else if (avgAccessibility < 3.5) weaknesses.push('Accessibility could be improved');

    if (mobileOptimizedPercent >= 0.8) strengths.push('Great mobile optimization');
    else if (mobileOptimizedPercent < 0.5) weaknesses.push('Limited mobile optimization');

    if (categoryDiversity >= 3) strengths.push('Good category diversity');
    else recommendations.push('Consider adding images from different categories');

    if (complexityBalance >= 0.6) strengths.push('Good balance of simple designs');
    else recommendations.push('Consider including more simple, clean designs');

    if (selectedImages.length < 3) recommendations.push('Consider selecting more images for better coverage');
    if (selectedImages.length > 6) recommendations.push('Consider reducing selection for better focus');

    return {
      overallScore: Math.round(overallScore * 20) / 20,
      strengths,
      weaknesses,
      recommendations
    };
  }

  // Get all images
  getAllImages(): ImageMetadata[] {
    return this.images;
  }

  // Get image by ID
  getImageById(id: string): ImageMetadata | undefined {
    return this.images.find(img => img.id === id);
  }
}

export const imageAnalyzer = new ImageAnalyzer();