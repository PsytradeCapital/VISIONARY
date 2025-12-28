/**
 * Theme Context for Mobile Theme Support
 * Task 10.6: Add mobile theme support with premium visual features
 * 
 * Features:
 * - Light/dark mode with animated transitions
 * - Customizable color schemes with premium visual elements
 * - Animated charts and interactive graphics for paid appeal
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Appearance, ColorSchemeName } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface ThemeColors {
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  card: string;
  text: string;
  textSecondary: string;
  border: string;
  notification: string;
  success: string;
  warning: string;
  error: string;
  gradient: {
    primary: string[];
    secondary: string[];
    accent: string[];
  };
}

export interface Theme {
  dark: boolean;
  colors: ThemeColors;
}

const lightTheme: Theme = {
  dark: false,
  colors: {
    primary: '#FF6B35',
    secondary: '#F7931E',
    background: '#F8F9FA',
    surface: '#FFFFFF',
    card: '#FFFFFF',
    text: '#1A1A1A',
    textSecondary: '#8E8E93',
    border: '#E5E5EA',
    notification: '#FF6B35',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#FF4444',
    gradient: {
      primary: ['#FF6B35', '#F7931E'],
      secondary: ['#667eea', '#764ba2'],
      accent: ['#4CAF50', '#8BC34A'],
    },
  },
};

const darkTheme: Theme = {
  dark: true,
  colors: {
    primary: '#FF6B35',
    secondary: '#F7931E',
    background: '#121212',
    surface: '#1E1E1E',
    card: '#2C2C2C',
    text: '#FFFFFF',
    textSecondary: '#B0B0B0',
    border: '#3C3C3C',
    notification: '#FF6B35',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#FF4444',
    gradient: {
      primary: ['#FF6B35', '#F7931E'],
      secondary: ['#667eea', '#764ba2'],
      accent: ['#4CAF50', '#8BC34A'],
    },
  },
};

export type ColorScheme = 'light' | 'dark' | 'auto';

interface ThemeContextType {
  theme: Theme;
  colorScheme: ColorScheme;
  setColorScheme: (scheme: ColorScheme) => void;
  toggleTheme: () => void;
  isAnimating: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [colorScheme, setColorSchemeState] = useState<ColorScheme>('auto');
  const [systemColorScheme, setSystemColorScheme] = useState<ColorSchemeName>(
    Appearance.getColorScheme()
  );
  const [isAnimating, setIsAnimating] = useState(false);

  // Determine current theme based on color scheme setting
  const getCurrentTheme = (): Theme => {
    if (colorScheme === 'auto') {
      return systemColorScheme === 'dark' ? darkTheme : lightTheme;
    }
    return colorScheme === 'dark' ? darkTheme : lightTheme;
  };

  const [theme, setTheme] = useState<Theme>(getCurrentTheme());

  // Load saved color scheme on app start
  useEffect(() => {
    loadColorScheme();
  }, []);

  // Listen to system color scheme changes
  useEffect(() => {
    const subscription = Appearance.addChangeListener(({ colorScheme: newColorScheme }) => {
      setSystemColorScheme(newColorScheme);
      if (colorScheme === 'auto') {
        updateTheme(newColorScheme === 'dark' ? darkTheme : lightTheme);
      }
    });

    return () => subscription?.remove();
  }, [colorScheme]);

  // Update theme when color scheme changes
  useEffect(() => {
    const newTheme = getCurrentTheme();
    updateTheme(newTheme);
  }, [colorScheme, systemColorScheme]);

  const loadColorScheme = async () => {
    try {
      const savedScheme = await AsyncStorage.getItem('colorScheme');
      if (savedScheme && ['light', 'dark', 'auto'].includes(savedScheme)) {
        setColorSchemeState(savedScheme as ColorScheme);
      }
    } catch (error) {
      console.error('Failed to load color scheme:', error);
    }
  };

  const updateTheme = (newTheme: Theme) => {
    setIsAnimating(true);
    setTheme(newTheme);
    
    // Animation duration
    setTimeout(() => {
      setIsAnimating(false);
    }, 300);
  };

  const setColorScheme = async (scheme: ColorScheme) => {
    try {
      await AsyncStorage.setItem('colorScheme', scheme);
      setColorSchemeState(scheme);
    } catch (error) {
      console.error('Failed to save color scheme:', error);
    }
  };

  const toggleTheme = () => {
    const newScheme = theme.dark ? 'light' : 'dark';
    setColorScheme(newScheme);
  };

  const contextValue: ThemeContextType = {
    theme,
    colorScheme,
    setColorScheme,
    toggleTheme,
    isAnimating,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Premium theme variants for paid users
export const premiumThemes = {
  ocean: {
    ...lightTheme,
    colors: {
      ...lightTheme.colors,
      gradient: {
        primary: ['#667eea', '#764ba2'],
        secondary: ['#f093fb', '#f5576c'],
        accent: ['#4facfe', '#00f2fe'],
      },
    },
  },
  sunset: {
    ...lightTheme,
    colors: {
      ...lightTheme.colors,
      gradient: {
        primary: ['#fa709a', '#fee140'],
        secondary: ['#a8edea', '#fed6e3'],
        accent: ['#ff9a9e', '#fecfef'],
      },
    },
  },
  forest: {
    ...lightTheme,
    colors: {
      ...lightTheme.colors,
      gradient: {
        primary: ['#134e5e', '#71b280'],
        secondary: ['#5f2c82', '#49a09d'],
        accent: ['#56ab2f', '#a8e6cf'],
      },
    },
  },
};