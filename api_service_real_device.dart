import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.100.93:8000'; // Real device IP
  // static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS simulator
  // static const String baseUrl = 'https://your-api-domain.com'; // Production
  
  late Dio _dio;
  static const FlutterSecureStorage _storage = FlutterSecureStorage();
  
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  
  ApiService._internal() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
      },
    ));
    
    // Add interceptor for authentication
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token expired, clear storage and redirect to login
          await clearToken();
        }
        handler.next(error);
      },
    ));
  }
  
  // Token management
  Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }
  
  Future<void> setToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
  }
  
  Future<void> clearToken() async {
    await _storage.delete(key: 'auth_token');
  }
  
  // Authentication
  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final formData = FormData.fromMap({
        'email': email,
        'password': password,
      });
      
      final response = await _dio.post('/api/auth/login', data: formData);
      
      if (response.data['access_token'] != null) {
        await setToken(response.data['access_token']);
      }
      
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> register(String email, String password) async {
    try {
      final formData = FormData.fromMap({
        'email': email,
        'password': password,
      });
      
      final response = await _dio.post('/api/auth/register', data: formData);
      
      if (response.data['access_token'] != null) {
        await setToken(response.data['access_token']);
      }
      
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> getCurrentUser() async {
    try {
      final response = await _dio.get('/api/auth/me');
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  // File Upload
  Future<Map<String, dynamic>> uploadDocument(File file) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          file.path,
          filename: file.path.split('/').last,
        ),
      });
      
      final response = await _dio.post('/api/upload/document', data: formData);
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> uploadText(String text) async {
    try {
      final formData = FormData.fromMap({
        'text': text,
      });
      
      final response = await _dio.post('/api/upload/text', data: formData);
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> uploadVoice(File audioFile) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          audioFile.path,
          filename: 'voice_recording.wav',
        ),
      });
      
      final response = await _dio.post('/api/upload/voice', data: formData);
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> getKnowledgeEntries() async {
    try {
      final response = await _dio.get('/api/upload/knowledge');
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  // Schedule
  Future<Map<String, dynamic>> getSchedules({String? timeframe}) async {
    try {
      final response = await _dio.get('/api/schedule/', queryParameters: {
        if (timeframe != null) 'timeframe': timeframe,
      });
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> generateSchedule(String timeframe, Map<String, dynamic> preferences) async {
    try {
      final response = await _dio.post('/api/schedule/generate', data: {
        'timeframe': timeframe,
        'preferences': preferences,
      });
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  // Progress
  Future<Map<String, dynamic>> getProgressOverview() async {
    try {
      final response = await _dio.get('/api/progress/overview');
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  Future<Map<String, dynamic>> updateVisionMetric(String visionId, String metricName, double newValue) async {
    try {
      final response = await _dio.put('/api/progress/vision/$visionId/metric', queryParameters: {
        'metric_name': metricName,
        'new_value': newValue,
      });
      return response.data;
    } catch (e) {
      throw _handleError(e);
    }
  }
  
  // Error handling
  String _handleError(dynamic error) {
    if (error is DioException) {
      if (error.response != null) {
        final data = error.response!.data;
        if (data is Map && data.containsKey('detail')) {
          return data['detail'].toString();
        }
        return 'Server error: ${error.response!.statusCode}';
      } else {
        return 'Network error: Please check your connection';
      }
    }
    return 'An unexpected error occurred';
  }
}