import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import '../../utils/theme.dart';
import '../../services/api_service.dart';
import 'dart:io';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _textController = TextEditingController();
  
  bool _isRecording = false;
  int _recordingDuration = 0;
  String? _recordingPath;
  
  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: AppTheme.primaryGradient,
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header
              const Padding(
                padding: EdgeInsets.all(24),
                child: Row(
                  children: [
                    Icon(Icons.cloud_upload, color: Colors.white, size: 32),
                    SizedBox(width: 16),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Smart Upload Portal',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          'AI-powered content processing',
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              
              // Content
              Expanded(
                child: Container(
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.vertical(
                      top: Radius.circular(30),
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      children: [
                        // Upload Options
                        Row(
                          children: [
                            Expanded(
                              child: _UploadOption(
                                icon: Icons.description,
                                title: 'Document',
                                subtitle: 'PDF, DOC, TXT',
                                color: Colors.blue,
                                onTap: _pickDocument,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _UploadOption(
                                icon: Icons.photo_camera,
                                title: 'Photo',
                                subtitle: 'Camera or Gallery',
                                color: Colors.green,
                                onTap: _pickImage,
                              ),
                            ),
                          ],
                        ),
                        
                        const SizedBox(height: 24),
                        
                        // Voice Recording
                        Container(
                          padding: const EdgeInsets.all(24),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [Colors.red[400]!, Colors.red[600]!],
                            ),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Column(
                            children: [
                              const Icon(
                                Icons.mic,
                                color: Colors.white,
                                size: 32,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                _isRecording ? 'Recording...' : 'Voice Recording',
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              if (_isRecording) ...[
                                const SizedBox(height: 8),
                                Text(
                                  '${_recordingDuration}s',
                                  style: const TextStyle(
                                    color: Colors.white70,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                              const SizedBox(height: 16),
                              ElevatedButton(
                                onPressed: _isRecording ? _stopRecording : _startRecording,
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.white,
                                  foregroundColor: Colors.red[600],
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(25),
                                  ),
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 32,
                                    vertical: 12,
                                  ),
                                ),
                                child: Text(
                                  _isRecording ? 'Stop Recording' : 'Start Recording',
                                  style: const TextStyle(fontWeight: FontWeight.w600),
                                ),
                              ),
                            ],
                          ),
                        ),
                        
                        const SizedBox(height: 24),
                        
                        // Text Input
                        Container(
                          padding: const EdgeInsets.all(20),
                          decoration: BoxDecoration(
                            color: Colors.grey[50],
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: Colors.grey[200]!),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Row(
                                children: [
                                  Icon(Icons.text_fields, color: AppTheme.primaryColor),
                                  SizedBox(width: 8),
                                  Text(
                                    'Text Input',
                                    style: AppTextStyles.heading3,
                                  ),
                                ],
                              ),
                              const SizedBox(height: 16),
                              TextField(
                                controller: _textController,
                                maxLines: 4,
                                decoration: const InputDecoration(
                                  hintText: 'Enter your goals, tasks, or notes here...',
                                  border: OutlineInputBorder(),
                                ),
                              ),
                              const SizedBox(height: 16),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton(
                                  onPressed: _processText,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppTheme.primaryColor,
                                    foregroundColor: Colors.white,
                                  ),
                                  child: const Text('Process Text'),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
  
  Future<void> _pickDocument() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'doc', 'docx', 'txt'],
      );
      
      if (result != null) {
        File file = File(result.files.single.path!);
        await _uploadDocument(file);
      }
    } catch (e) {
      _showError('Failed to pick document: $e');
    }
  }
  
  Future<void> _pickImage() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(source: ImageSource.gallery);
      
      if (image != null) {
        File file = File(image.path);
        await _uploadDocument(file);
      }
    } catch (e) {
      _showError('Failed to pick image: $e');
    }
  }
  
  Future<void> _startRecording() async {
    try {
      if (await Permission.microphone.request().isGranted) {
        setState(() {
          _isRecording = true;
          _recordingDuration = 0;
          _recordingPath = 'temp_recording.wav';
        });
        
        _startTimer();
      } else {
        _showError('Microphone permission denied');
      }
    } catch (e) {
      _showError('Failed to start recording: $e');
    }
  }
  
  Future<void> _stopRecording() async {
    try {
      setState(() {
        _isRecording = false;
      });
      
      _showSuccess('Recording completed (demo mode)');
    } catch (e) {
      _showError('Failed to stop recording: $e');
    }
  }
  
  void _startTimer() {
    Future.delayed(const Duration(seconds: 1), () {
      if (_isRecording) {
        setState(() {
          _recordingDuration++;
        });
        _startTimer();
      }
    });
  }
  
  Future<void> _uploadDocument(File file) async {
    try {
      _showLoading('Uploading document...');
      final response = await _apiService.uploadDocument(file);
      Navigator.pop(context);
      
      if (response['success'] == true) {
        _showSuccess('Document uploaded and processed successfully!');
      } else {
        _showError('Upload failed');
      }
    } catch (e) {
      Navigator.pop(context);
      _showError('Upload failed: $e');
    }
  }
  
  Future<void> _processText() async {
    if (_textController.text.trim().isEmpty) {
      _showError('Please enter some text');
      return;
    }
    
    try {
      _showLoading('Processing text...');
      final response = await _apiService.uploadText(_textController.text.trim());
      Navigator.pop(context);
      
      if (response['success'] == true) {
        _showSuccess('Text processed successfully!');
        _textController.clear();
      } else {
        _showError('Text processing failed');
      }
    } catch (e) {
      Navigator.pop(context);
      _showError('Text processing failed: $e');
    }
  }
  
  void _showLoading(String message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        content: Row(
          children: [
            const CircularProgressIndicator(),
            const SizedBox(width: 16),
            Text(message),
          ],
        ),
      ),
    );
  }
  
  void _showSuccess(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.green,
      ),
    );
  }
  
  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }
}

class _UploadOption extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  
  const _UploadOption({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.2)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 12),
            Text(
              title,
              style: AppTextStyles.body1.copyWith(
                fontWeight: FontWeight.w600,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              subtitle,
              style: AppTextStyles.caption,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}