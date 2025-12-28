/**
 * Profile Screen with Premium Visual Features
 * User profile management with theme support
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Switch,
  Image,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSelector } from 'react-redux';

import { RootState } from '../store/store';
import { useTheme } from '../contexts/ThemeContext';

interface ProfileOption {
  id: string;
  title: string;
  subtitle?: string;
  icon: string;
  type: 'navigation' | 'toggle' | 'action';
  value?: boolean;
  onPress?: () => void;
  onToggle?: (value: boolean) => void;
}

const ProfileScreen: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const { theme, colorScheme, setColorScheme, toggleTheme } = useTheme();
  const [notifications, setNotifications] = useState(true);
  const [biometrics, setBiometrics] = useState(false);

  const handleThemeToggle = (value: boolean) => {
    setColorScheme(value ? 'dark' : 'light');
  };

  const profileOptions: ProfileOption[] = [
    {
      id: 'personal_info',
      title: 'Personal Information',
      subtitle: 'Update your profile details',
      icon: 'person',
      type: 'navigation',
      onPress: () => Alert.alert('Coming Soon', 'Personal information editing will be available soon!'),
    },
    {
      id: 'goals',
      title: 'Goals & Preferences',
      subtitle: 'Customize your experience',
      icon: 'target',
      type: 'navigation',
      onPress: () => Alert.alert('Coming Soon', 'Goals customization will be available soon!'),
    },
    {
      id: 'notifications',
      title: 'Push Notifications',
      subtitle: 'Manage your notification preferences',
      icon: 'notifications',
      type: 'toggle',
      value: notifications,
      onToggle: setNotifications,
    },
    {
      id: 'dark_mode',
      title: 'Dark Mode',
      subtitle: 'Switch between light and dark themes',
      icon: 'moon',
      type: 'toggle',
      value: theme.dark,
      onToggle: handleThemeToggle,
    },
    {
      id: 'biometrics',
      title: 'Biometric Authentication',
      subtitle: 'Use fingerprint or face recognition',
      icon: 'finger-print',
      type: 'toggle',
      value: biometrics,
      onToggle: setBiometrics,
    },
    {
      id: 'data_export',
      title: 'Export Data',
      subtitle: 'Download your personal data',
      icon: 'download',
      type: 'action',
      onPress: () => Alert.alert('Export Data', 'Your data export will be prepared and sent to your email.'),
    },
    {
      id: 'privacy',
      title: 'Privacy & Security',
      subtitle: 'Manage your privacy settings',
      icon: 'shield-checkmark',
      type: 'navigation',
      onPress: () => Alert.alert('Coming Soon', 'Privacy settings will be available soon!'),
    },
    {
      id: 'help',
      title: 'Help & Support',
      subtitle: 'Get help and contact support',
      icon: 'help-circle',
      type: 'navigation',
      onPress: () => Alert.alert('Coming Soon', 'Help center will be available soon!'),
    },
    {
      id: 'about',
      title: 'About',
      subtitle: 'App version and information',
      icon: 'information-circle',
      type: 'navigation',
      onPress: () => Alert.alert('About', 'Visionary AI Personal Scheduler\nVersion 1.0.0\n\nBuilt with ❤️ for productivity'),
    },
  ];

  const renderProfileHeader = () => (
    <LinearGradient
      colors={['#667eea', '#764ba2']}
      style={styles.profileHeader}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
    >
      <View style={styles.profileImageContainer}>
        <Image
          source={{
            uri: user?.avatar || 'https://via.placeholder.com/100x100/CCCCCC/FFFFFF?text=User'
          }}
          style={styles.profileImage}
        />
        <TouchableOpacity style={styles.editImageButton}>
          <Ionicons name="camera" size={16} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
      
      <Text style={styles.profileName}>{user?.name || 'User Name'}</Text>
      <Text style={styles.profileEmail}>{user?.email || 'user@example.com'}</Text>
      
      <View style={styles.profileStats}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>127</Text>
          <Text style={styles.statLabel}>Tasks Completed</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>23</Text>
          <Text style={styles.statLabel}>Goals Achieved</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>89%</Text>
          <Text style={styles.statLabel}>Success Rate</Text>
        </View>
      </View>
    </LinearGradient>
  );

  const renderProfileOption = (option: ProfileOption) => (
    <TouchableOpacity
      key={option.id}
      style={styles.optionItem}
      onPress={option.onPress}
      disabled={option.type === 'toggle'}
    >
      <View style={styles.optionContent}>
        <View style={styles.optionIcon}>
          <Ionicons name={option.icon as any} size={24} color="#FF6B35" />
        </View>
        <View style={styles.optionText}>
          <Text style={styles.optionTitle}>{option.title}</Text>
          {option.subtitle && (
            <Text style={styles.optionSubtitle}>{option.subtitle}</Text>
          )}
        </View>
        <View style={styles.optionAction}>
          {option.type === 'toggle' ? (
            <Switch
              value={option.value}
              onValueChange={option.onToggle}
              trackColor={{ false: '#E5E5EA', true: '#FF6B35' }}
              thumbColor="#FFFFFF"
            />
          ) : (
            <Ionicons name="chevron-forward" size={20} color="#8E8E93" />
          )}
        </View>
      </View>
    </TouchableOpacity>
  );

  const renderPremiumSection = () => (
    <View style={styles.premiumSection}>
      <LinearGradient
        colors={['#FFD700', '#FFA500']}
        style={styles.premiumCard}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.premiumContent}>
          <Ionicons name="star" size={32} color="#FFFFFF" />
          <Text style={styles.premiumTitle}>Upgrade to Premium</Text>
          <Text style={styles.premiumSubtitle}>
            Unlock AI-powered insights, unlimited uploads, and premium visual analytics
          </Text>
          <TouchableOpacity style={styles.premiumButton}>
            <Text style={styles.premiumButtonText}>Upgrade Now</Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>
    </View>
  );

  const renderDangerZone = () => (
    <View style={styles.dangerZone}>
      <Text style={styles.dangerZoneTitle}>Account Actions</Text>
      
      <TouchableOpacity
        style={styles.dangerOption}
        onPress={() => Alert.alert(
          'Sign Out',
          'Are you sure you want to sign out?',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Sign Out', style: 'destructive', onPress: () => console.log('Sign out') }
          ]
        )}
      >
        <Ionicons name="log-out" size={24} color="#FF4444" />
        <Text style={styles.dangerOptionText}>Sign Out</Text>
      </TouchableOpacity>
      
      <TouchableOpacity
        style={styles.dangerOption}
        onPress={() => Alert.alert(
          'Delete Account',
          'This action cannot be undone. All your data will be permanently deleted.',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Delete', style: 'destructive', onPress: () => console.log('Delete account') }
          ]
        )}
      >
        <Ionicons name="trash" size={24} color="#FF4444" />
        <Text style={styles.dangerOptionText}>Delete Account</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {renderProfileHeader()}
        {renderPremiumSection()}
        
        <View style={styles.optionsSection}>
          {profileOptions.map(renderProfileOption)}
        </View>
        
        {renderDangerZone()}
        
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Made with ❤️ for productivity enthusiasts
          </Text>
          <Text style={styles.versionText}>Version 1.0.0</Text>
        </View>
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
  profileHeader: {
    alignItems: 'center',
    paddingVertical: 32,
    paddingHorizontal: 16,
  },
  profileImageContainer: {
    position: 'relative',
    marginBottom: 16,
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 4,
    borderColor: '#FFFFFF',
  },
  editImageButton: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#FF6B35',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#FFFFFF',
  },
  profileName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  profileEmail: {
    fontSize: 16,
    color: '#FFFFFF',
    opacity: 0.9,
    marginBottom: 24,
  },
  profileStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statItem: {
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.8,
  },
  statDivider: {
    width: 1,
    height: 32,
    backgroundColor: '#FFFFFF',
    opacity: 0.3,
  },
  premiumSection: {
    margin: 16,
  },
  premiumCard: {
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  premiumContent: {
    alignItems: 'center',
  },
  premiumTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginTop: 8,
    marginBottom: 8,
  },
  premiumSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    textAlign: 'center',
    opacity: 0.9,
    marginBottom: 16,
    lineHeight: 20,
  },
  premiumButton: {
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 24,
  },
  premiumButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFA500',
  },
  optionsSection: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 16,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  optionItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  optionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 16,
  },
  optionIcon: {
    width: 40,
    alignItems: 'center',
  },
  optionText: {
    flex: 1,
    marginLeft: 12,
  },
  optionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 2,
  },
  optionSubtitle: {
    fontSize: 14,
    color: '#8E8E93',
  },
  optionAction: {
    marginLeft: 12,
  },
  dangerZone: {
    margin: 16,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  dangerZoneTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FF4444',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  dangerOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  dangerOptionText: {
    fontSize: 16,
    color: '#FF4444',
    marginLeft: 12,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 32,
    paddingHorizontal: 16,
  },
  footerText: {
    fontSize: 14,
    color: '#8E8E93',
    textAlign: 'center',
    marginBottom: 8,
  },
  versionText: {
    fontSize: 12,
    color: '#CCCCCC',
  },
});

export default ProfileScreen;