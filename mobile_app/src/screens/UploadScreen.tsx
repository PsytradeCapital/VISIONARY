/**
 * Mobile-Optimized Upload Portal with Multi-Modal Input
 * Task 10.2: Add mobile-optimized upload portal with multi-modal input
 * 
 * Features:
 * - Mobile drag-and-drop file upload with camera integration
 * - Native voice recording with real-time transcription
 * - Mobile-specific text input with predictive suggestions
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
  Alert,
  TextInput,
  Animated,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import * as DocumentPicker from 'expo-document-picker';
import * as ImagePicker from 'expo-image-picker';
import { Audio } from 'expo-av';
import { useDispatch, useSelector } from 'react-redux';

import { RootState } from '../store/store';
import { uploadFile, uploadVoice, uploadText } from '../store/slices/uploadSlice';
import { VoiceRecordingService } from '../services/VoiceRecordingService';
import { PredictiveTextService } from '../services/PredictiveTextService';

const { width, height } = Dimensions.get('window');

interface UploadOption {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  colors: string[];
  onPress: () => void;
}

const UploadScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { uploading, progress, error } = useSelector((state: RootState) => state.upload);
  
  // Voice recording state
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [transcription, setTranscription] = useState('');
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  
  // Text input state
  const [textInput, setTextInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  
  // Animation values
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const recordingAnim = useRef(new Animated.Value(0)).current;
  
  // Services
  const voiceService = useRef(new VoiceRecordingService()).current;
  const textService = useRef(new PredictiveTextService()).current;

  useEffect(() => {
    requestPermissions();
    return () => {
      if (recording) {
        recording.stopAndUnloadAsync();
      }
    };
  }, []);

  useEffect(() => {
    if (isRecording) {
      startPulseAnimation();
      startRecordingTimer();
    } else {
      stopPulseAnimation();
    }
  }, [isRecording]);

  const requestPermissions = async () => {
    try {
      // Request audio recording permission
      const audioPermission = await Audio.requestPermissionsAsync();
      if (!audioPermission.granted) {
        Alert.alert('Permission Required', 'Audio recording permission is needed for voice input.');
      }

      // Request camera permission
      const cameraPermission = await ImagePicker.requestCameraPermissionsAsync();
      if (!cameraPermission.granted) {
        Alert.alert('Permission Required', 'Camera permission is needed for document capture.');
      }

      // Request media library permission
      const mediaPermission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!mediaPermission.granted) {
        Alert.alert('Permission Required', 'Media library permission is needed for file uploads.');
      }
    } catch (error) {
      console.error('Failed to request permissions:', error);
    }
  };

  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const stopPulseAnimation = () => {
    pulseAnim.stopAnimation();
    Animated.timing(pulseAnim, {
      toValue: 1,
      duration: 200,
      useNativeDriver: true,
    }).start();
  };

  const startRecordingTimer = () => {
    const timer = setInterval(() => {
      setRecordingDuration(prev => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  };

  const handleFileUpload = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: '*/*',
        copyToCacheDirectory: true,
        multiple: false,
      });

      if (!result.canceled && result.assets[0]) {
        const file = result.assets[0];
        // @ts-ignore
        await dispatch(uploadFile({
          uri: file.uri,
          name: file.name,
          type: file.mimeType || 'application/octet-stream',
          size: file.size,
        }));
      }
    } catch (error) {
      console.error('File upload failed:', error);
      Alert.alert('Upload Failed', 'Failed to upload file. Please try again.');
    }
  };

  const handleCameraCapture = async () => {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        const image = result.assets[0];
        // @ts-ignore
        await dispatch(uploadFile({
          uri: image.uri,
          name: `camera_capture_${Date.now()}.jpg`,
          type: 'image/jpeg',
          size: image.fileSize || 0,
        }));
      }
    } catch (error) {
      console.error('Camera capture failed:', error);
      Alert.alert('Capture Failed', 'Failed to capture image. Please try again.');
    }
  };

  const handlePhotoLibrary = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
        allowsMultipleSelection: false,
      });

      if (!result.canceled && result.assets[0]) {
        const media = result.assets[0];
        // @ts-ignore
        await dispatch(uploadFile({
          uri: media.uri,
          name: `library_${Date.now()}.${media.type === 'video' ? 'mp4' : 'jpg'}`,
          type: media.type === 'video' ? 'video/mp4' : 'image/jpeg',
          size: media.fileSize || 0,
        }));
      }
    } catch (error) {
      console.error('Photo library selection failed:', error);
      Alert.alert('Selection Failed', 'Failed to select media. Please try again.');
    }
  };

  const startVoiceRecording = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording: newRecording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );

      setRecording(newRecording);
      setIsRecording(true);
      setRecordingDuration(0);
      setTranscription('');

      // Start real-time transcription
      voiceService.startRealTimeTranscription((text) => {
        setTranscription(text);
      });

    } catch (error) {
      console.error('Failed to start recording:', error);
      Alert.alert('Recording Failed', 'Failed to start voice recording. Please try again.');
    }
  };

  const stopVoiceRecording = async () => {
    try {
      if (!recording) return;

      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      
      const uri = recording.getURI();
      if (uri) {
        // Upload voice recording
        // @ts-ignore
        await dispatch(uploadVoice({
          uri,
          duration: recordingDuration,
          transcription,
        }));
      }

      setRecording(null);
      setRecordingDuration(0);
      voiceService.stopRealTimeTranscription();

    } catch (error) {
      console.error('Failed to stop recording:', error);
      Alert.alert('Recording Failed', 'Failed to process voice recording. Please try again.');
    }
  };

  const handleTextInput = async (text: string) => {
    setTextInput(text);
    
    if (text.length > 2) {
      try {
        const predictions = await textService.getPredictions(text);
        setSuggestions(predictions);
        setShowSuggestions(predictions.length > 0);
      } catch (error) {
        console.error('Failed to get text predictions:', error);
      }
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSuggestionSelect = (suggestion: string) => {
    setTextInput(suggestion);
    setShowSuggestions(false);
  };

  const handleTextSubmit = async () => {
    if (textInput.trim()) {
      try {
        // @ts-ignore
        await dispatch(uploadText({
          content: textInput.trim(),
          type: 'manual_input',
        }));
        setTextInput('');
        setShowSuggestions(false);
      } catch (error) {
        console.error('Text upload failed:', error);
        Alert.alert('Upload Failed', 'Failed to upload text. Please try again.');
      }
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const uploadOptions: UploadOption[] = [
    {
      id: 'file',
      title: 'Upload File',
      subtitle: 'Documents, PDFs, Images',
      icon: 'document-text',
      colors: ['#4CAF50', '#8BC34A'],
      onPress: handleFileUpload,
    },
    {
      id: 'camera',
      title: 'Camera Capture',
      subtitle: 'Take photo of document',
      icon: 'camera',
      colors: ['#2196F3', '#03DAC6'],
      onPress: handleCameraCapture,
    },
    {
      id: 'library',
      title: 'Photo Library',
      subtitle: 'Select from gallery',
      icon: 'images',
      colors: ['#9C27B0', '#E91E63'],
      onPress: handlePhotoLibrary,
    },
  ];

  const renderUploadOptions = () => (
    <View style={styles.uploadOptionsSection}>
      <Text style={styles.sectionTitle}>Upload Content</Text>
      <View style={styles.uploadOptionsGrid}>
        {uploadOptions.map((option) => (
          <TouchableOpacity
            key={option.id}
            style={styles.uploadOptionCard}
            onPress={option.onPress}
            disabled={uploading}
          >
            <LinearGradient
              colors={option.colors}
              style={styles.uploadOptionGradient}
            >
              <Ionicons name={option.icon as any} size={32} color="#FFFFFF" />
              <Text style={styles.uploadOptionTitle}>{option.title}</Text>
              <Text style={styles.uploadOptionSubtitle}>{option.subtitle}</Text>
            </LinearGradient>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderVoiceRecording = () => (
    <View style={styles.voiceSection}>
      <Text style={styles.sectionTitle}>Voice Input</Text>
      
      <View style={styles.voiceRecordingContainer}>
        <TouchableOpacity
          style={styles.recordButton}
          onPress={isRecording ? stopVoiceRecording : startVoiceRecording}
          disabled={uploading}
        >
          <Animated.View style={[
            styles.recordButtonInner,
            { transform: [{ scale: pulseAnim }] }
          ]}>
            <LinearGradient
              colors={isRecording ? ['#FF4444', '#FF6666'] : ['#FF6B35', '#F7931E']}
              style={styles.recordButtonGradient}
            >
              <Ionicons 
                name={isRecording ? 'stop' : 'mic'} 
                size={32} 
                color="#FFFFFF" 
              />
            </LinearGradient>
          </Animated.View>
        </TouchableOpacity>

        {isRecording && (
          <View style={styles.recordingInfo}>
            <Text style={styles.recordingDuration}>
              {formatDuration(recordingDuration)}
            </Text>
            <Text style={styles.recordingStatus}>Recording...</Text>
          </View>
        )}

        {transcription && (
          <View style={styles.transcriptionContainer}>
            <Text style={styles.transcriptionLabel}>Live Transcription:</Text>
            <Text style={styles.transcriptionText}>{transcription}</Text>
          </View>
        )}
      </View>
    </View>
  );

  const renderTextInput = () => (
    <View style={styles.textSection}>
      <Text style={styles.sectionTitle}>Text Input</Text>
      
      <View style={styles.textInputContainer}>
        <TextInput
          style={styles.textInput}
          placeholder="Type your content here..."
          placeholderTextColor="#8E8E93"
          value={textInput}
          onChangeText={handleTextInput}
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />
        
        {showSuggestions && suggestions.length > 0 && (
          <View style={styles.suggestionsContainer}>
            <Text style={styles.suggestionsLabel}>Suggestions:</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {suggestions.map((suggestion, index) => (
                <TouchableOpacity
                  key={index}
                  style={styles.suggestionChip}
                  onPress={() => handleSuggestionSelect(suggestion)}
                >
                  <Text style={styles.suggestionText}>{suggestion}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}
        
        <TouchableOpacity
          style={styles.submitButton}
          onPress={handleTextSubmit}
          disabled={!textInput.trim() || uploading}
        >
          <LinearGradient
            colors={['#4CAF50', '#8BC34A']}
            style={styles.submitButtonGradient}
          >
            <Ionicons name="send" size={20} color="#FFFFFF" />
            <Text style={styles.submitButtonText}>Submit Text</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderUploadProgress = () => {
    if (!uploading) return null;

    return (
      <View style={styles.progressContainer}>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
        <Text style={styles.progressText}>Uploading... {progress}%</Text>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Upload Content</Text>
        <Text style={styles.headerSubtitle}>
          Share documents, voice notes, or text
        </Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {renderUploadOptions()}
        {renderVoiceRecording()}
        {renderTextInput()}
        {renderUploadProgress()}
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
    paddingHorizontal: 16,
    paddingVertical: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#8E8E93',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 16,
  },
  uploadOptionsSection: {
    padding: 16,
  },
  uploadOptionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  uploadOptionCard: {
    width: (width - 48) / 2,
    marginBottom: 16,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  uploadOptionGradient: {
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 120,
  },
  uploadOptionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginTop: 8,
    textAlign: 'center',
  },
  uploadOptionSubtitle: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.9,
    marginTop: 4,
    textAlign: 'center',
  },
  voiceSection: {
    padding: 16,
  },
  voiceRecordingContainer: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  recordButton: {
    marginBottom: 16,
  },
  recordButtonInner: {
    width: 80,
    height: 80,
    borderRadius: 40,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
  },
  recordButtonGradient: {
    width: '100%',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'center',
  },
  recordingInfo: {
    alignItems: 'center',
    marginBottom: 16,
  },
  recordingDuration: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF4444',
    marginBottom: 4,
  },
  recordingStatus: {
    fontSize: 14,
    color: '#8E8E93',
  },
  transcriptionContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    width: '100%',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  transcriptionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  transcriptionText: {
    fontSize: 16,
    color: '#1A1A1A',
    lineHeight: 24,
  },
  textSection: {
    padding: 16,
  },
  textInputContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  textInput: {
    fontSize: 16,
    color: '#1A1A1A',
    minHeight: 100,
    textAlignVertical: 'top',
    marginBottom: 16,
  },
  suggestionsContainer: {
    marginBottom: 16,
  },
  suggestionsLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  suggestionChip: {
    backgroundColor: '#F0F0F0',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 8,
  },
  suggestionText: {
    fontSize: 14,
    color: '#1A1A1A',
  },
  submitButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  submitButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  submitButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 8,
  },
  progressContainer: {
    margin: 16,
    padding: 16,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  progressBar: {
    height: 4,
    backgroundColor: '#E5E5EA',
    borderRadius: 2,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
    borderRadius: 2,
  },
  progressText: {
    fontSize: 14,
    color: '#1A1A1A',
    textAlign: 'center',
  },
});

export default UploadScreen;