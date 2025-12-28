"""
Mobile-optimized voice input processing with cloud-based speech-to-text
Task 3.2: Add mobile-optimized voice input processing
"""

import asyncio
import io
import tempfile
import os
from typing import Tuple, Dict, Any, Optional
from pathlib import Path
import wave
from pydantic import BaseModel

# Google Cloud Speech-to-Text (when available)
try:
    from google.cloud import speech
    GOOGLE_SPEECH_AVAILABLE = True
except ImportError:
    GOOGLE_SPEECH_AVAILABLE = False

# Alternative speech recognition libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

from ..core.config import settings

class VoiceProcessor:
    """Mobile-optimized voice input processing with cloud-based speech-to-text"""
    
    def __init__(self):
        # Mobile audio optimization settings
        self.mobile_sample_rate = 16000  # Optimal for speech recognition
        self.mobile_channels = 1  # Mono for better processing
        self.mobile_bit_depth = 16
        
        # Noise reduction settings
        self.noise_reduction_enabled = True
        self.silence_threshold = 500  # Adjust based on testing
        
        # Cloud processing settings
        self.google_speech_client = None
        if GOOGLE_SPEECH_AVAILABLE and hasattr(settings, 'GOOGLE_CLOUD_CREDENTIALS'):
            try:
                self.google_speech_client = speech.SpeechClient()
            except Exception as e:
                print(f"Failed to initialize Google Speech client: {e}")
        
        # Fallback speech recognition
        self.sr_recognizer = None
        if SPEECH_RECOGNITION_AVAILABLE:
            self.sr_recognizer = sr.Recognizer()
        
        # Supported audio formats
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac']
        
        # Mobile optimization settings
        self.mobile_chunk_size = 1024  # Process in small chunks for mobile
        self.mobile_timeout = 30  # Maximum processing time for mobile
        
    async def transcribe_audio(
        self, 
        audio_content: bytes, 
        filename: str,
        mobile_optimized: bool = True,
        language_code: str = "en-US"
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Transcribe audio with mobile optimization and cloud processing
        
        Args:
            audio_content: Raw audio bytes
            filename: Original filename
            mobile_optimized: Enable mobile-specific optimizations
            language_code: Language for transcription
        """
        try:
            # Prepare metadata
            metadata = {
                "original_filename": filename,
                "file_size": len(audio_content),
                "mobile_optimized": mobile_optimized,
                "language_code": language_code,
                "processing_method": "unknown"
            }
            
            # Optimize audio for mobile if needed
            if mobile_optimized:
                audio_content, optimization_metadata = await self._optimize_audio_for_mobile(
                    audio_content, filename
                )
                metadata.update(optimization_metadata)
            
            # Try Google Cloud Speech-to-Text first (best quality)
            if self.google_speech_client:
                try:
                    transcription, google_metadata = await self._transcribe_with_google_cloud(
                        audio_content, language_code
                    )
                    metadata.update(google_metadata)
                    metadata["processing_method"] = "google_cloud_speech"
                    return transcription, metadata
                except Exception as e:
                    print(f"Google Cloud Speech failed: {e}")
                    metadata["google_cloud_error"] = str(e)
            
            # Fallback to speech_recognition library
            if self.sr_recognizer:
                try:
                    transcription, sr_metadata = await self._transcribe_with_speech_recognition(
                        audio_content, language_code
                    )
                    metadata.update(sr_metadata)
                    metadata["processing_method"] = "speech_recognition_fallback"
                    return transcription, metadata
                except Exception as e:
                    print(f"Speech recognition fallback failed: {e}")
                    metadata["speech_recognition_error"] = str(e)
            
            # If all methods fail
            return "Audio transcription failed - no available speech recognition service", metadata
            
        except Exception as e:
            return f"Error processing audio: {str(e)}", {
                "error": True,
                "error_message": str(e),
                "filename": filename
            }
    
    async def _optimize_audio_for_mobile(
        self, 
        audio_content: bytes, 
        filename: str
    ) -> Tuple[bytes, Dict[str, Any]]:
        """Optimize audio for mobile processing and speech recognition"""
        try:
            # Create temporary file for processing
            with tempfile.NamedTemporaryFile(suffix=Path(filename).suffix, delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            
            try:
                # Convert to WAV format for processing
                wav_path = temp_path + ".wav"
                
                # Use ffmpeg if available, otherwise basic conversion
                if self._is_ffmpeg_available():
                    await self._convert_with_ffmpeg(temp_path, wav_path)
                else:
                    # Basic conversion for WAV files
                    if filename.lower().endswith('.wav'):
                        wav_path = temp_path
                    else:
                        # Copy as-is and hope for the best
                        wav_path = temp_path
                
                # Read optimized audio
                with open(wav_path, 'rb') as f:
                    optimized_content = f.read()
                
                # Analyze audio properties
                metadata = await self._analyze_audio_properties(optimized_content)
                metadata["optimization_applied"] = True
                
                return optimized_content, metadata
                
            finally:
                # Clean up temporary files
                try:
                    os.unlink(temp_path)
                    if wav_path != temp_path and os.path.exists(wav_path):
                        os.unlink(wav_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"Audio optimization failed: {e}")
            return audio_content, {
                "optimization_applied": False,
                "optimization_error": str(e)
            }
    
    def _is_ffmpeg_available(self) -> bool:
        """Check if ffmpeg is available for audio conversion"""
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    async def _convert_with_ffmpeg(self, input_path: str, output_path: str):
        """Convert audio using ffmpeg"""
        import subprocess
        
        # FFmpeg command for mobile optimization
        cmd = [
            'ffmpeg', '-i', input_path,
            '-ar', str(self.mobile_sample_rate),  # Sample rate
            '-ac', str(self.mobile_channels),     # Channels (mono)
            '-sample_fmt', 's16',                 # 16-bit samples
            '-y',                                 # Overwrite output
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg conversion failed: {stderr.decode()}")
    
    async def _analyze_audio_properties(self, audio_content: bytes) -> Dict[str, Any]:
        """Analyze audio properties for metadata"""
        try:
            # Basic analysis - in a real implementation, you'd use librosa or similar
            metadata = {
                "file_size_bytes": len(audio_content),
                "analysis_method": "basic"
            }
            
            # Try to read as WAV for basic properties
            try:
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_file.write(audio_content)
                    temp_path = temp_file.name
                
                try:
                    with wave.open(temp_path, 'rb') as wav_file:
                        metadata.update({
                            "sample_rate": wav_file.getframerate(),
                            "channels": wav_file.getnchannels(),
                            "sample_width": wav_file.getsampwidth(),
                            "duration_seconds": wav_file.getnframes() / wav_file.getframerate(),
                            "total_frames": wav_file.getnframes()
                        })
                finally:
                    os.unlink(temp_path)
                    
            except Exception as wav_error:
                metadata["wav_analysis_error"] = str(wav_error)
            
            return metadata
            
        except Exception as e:
            return {
                "analysis_error": str(e),
                "file_size_bytes": len(audio_content)
            }
    
    async def _transcribe_with_google_cloud(
        self, 
        audio_content: bytes, 
        language_code: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Transcribe using Google Cloud Speech-to-Text"""
        try:
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.mobile_sample_rate,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_word_confidence=True,
                enable_word_time_offsets=True,
                model="latest_long",  # Best for longer audio
                use_enhanced=True     # Enhanced model for better accuracy
            )
            
            audio = speech.RecognitionAudio(content=audio_content)
            
            # Perform transcription
            response = self.google_speech_client.recognize(config=config, audio=audio)
            
            # Process results
            transcription = ""
            confidence_scores = []
            word_count = 0
            
            for result in response.results:
                transcription += result.alternatives[0].transcript + " "
                confidence_scores.append(result.alternatives[0].confidence)
                
                # Count words with confidence data
                for word_info in result.alternatives[0].words:
                    word_count += 1
            
            metadata = {
                "confidence_avg": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "confidence_min": min(confidence_scores) if confidence_scores else 0,
                "confidence_max": max(confidence_scores) if confidence_scores else 0,
                "word_count": word_count,
                "results_count": len(response.results)
            }
            
            return transcription.strip(), metadata
            
        except Exception as e:
            raise Exception(f"Google Cloud Speech transcription failed: {str(e)}")
    
    async def _transcribe_with_speech_recognition(
        self, 
        audio_content: bytes, 
        language_code: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Transcribe using speech_recognition library (fallback)"""
        try:
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            
            try:
                # Load audio file
                with sr.AudioFile(temp_path) as source:
                    # Adjust for ambient noise
                    self.sr_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Record audio
                    audio_data = self.sr_recognizer.record(source)
                
                # Try multiple recognition services
                transcription = None
                service_used = None
                
                # Try Google Web Speech API (free tier)
                try:
                    transcription = self.sr_recognizer.recognize_google(
                        audio_data, language=language_code.replace('-', '_')
                    )
                    service_used = "google_web_speech"
                except sr.RequestError:
                    pass
                except sr.UnknownValueError:
                    pass
                
                # Try Sphinx (offline) as last resort
                if not transcription:
                    try:
                        transcription = self.sr_recognizer.recognize_sphinx(audio_data)
                        service_used = "sphinx_offline"
                    except sr.RequestError:
                        pass
                    except sr.UnknownValueError:
                        pass
                
                if not transcription:
                    raise Exception("No speech recognition service could process the audio")
                
                metadata = {
                    "service_used": service_used,
                    "word_count": len(transcription.split()),
                    "character_count": len(transcription)
                }
                
                return transcription, metadata
                
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            raise Exception(f"Speech recognition fallback failed: {str(e)}")
    
    async def enhance_audio_quality(self, audio_content: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """Enhance audio quality for better speech recognition"""
        try:
            # This is a placeholder for audio enhancement
            # In a real implementation, you might use:
            # - Noise reduction algorithms
            # - Audio normalization
            # - Spectral subtraction
            # - Wiener filtering
            
            metadata = {
                "enhancement_applied": False,
                "enhancement_method": "placeholder",
                "original_size": len(audio_content),
                "enhanced_size": len(audio_content)
            }
            
            # For now, return original audio
            return audio_content, metadata
            
        except Exception as e:
            return audio_content, {
                "enhancement_error": str(e),
                "enhancement_applied": False
            }
    
    async def detect_speech_segments(self, audio_content: bytes) -> Dict[str, Any]:
        """Detect speech segments in audio (Voice Activity Detection)"""
        try:
            # Placeholder for VAD implementation
            # In a real implementation, you might use:
            # - WebRTC VAD
            # - Deep learning models
            # - Energy-based detection
            
            return {
                "speech_segments": [
                    {"start": 0.0, "end": 10.0, "confidence": 0.8}
                ],
                "total_speech_duration": 10.0,
                "silence_duration": 0.0,
                "speech_ratio": 1.0,
                "vad_method": "placeholder"
            }
            
        except Exception as e:
            return {
                "vad_error": str(e),
                "speech_segments": []
            }
    
    async def get_supported_languages(self) -> Dict[str, Any]:
        """Get list of supported languages for transcription"""
        return {
            "google_cloud_languages": [
                "en-US", "en-GB", "es-ES", "fr-FR", "de-DE", 
                "it-IT", "pt-BR", "ru-RU", "ja-JP", "ko-KR", "zh-CN"
            ],
            "speech_recognition_languages": [
                "en-US", "en-GB", "es-ES", "fr-FR", "de-DE"
            ],
            "default_language": "en-US",
            "auto_detect_available": False  # Would require additional implementation
        }