"""
Speech recognition module - Integrating Vosk API for offline speech-to-text
"""

import json
import sys
import os
from typing import Optional, Any

# Conditional imports - only import if available
VOSK_AVAILABLE = False
PYAUDIO_AVAILABLE = False

try:
    import vosk
    VOSK_AVAILABLE = True
except ImportError:
    vosk = None

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None

class SpeechRecognizer:
    """Speech recognizer based on Vosk API"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the speech recognizer
        
        Args:
            model_path: Path to Vosk model, if None uses default model
        """
        if not VOSK_AVAILABLE or not PYAUDIO_AVAILABLE:
            raise ImportError("Vosk or PyAudio not available. Please install with: pip install vosk pyaudio")
        
        # Initialize Vosk model
        try:
            if model_path and os.path.exists(model_path):
                self.model = vosk.Model(model_path)  # type: ignore
            else:
                # Try to use default model - handle potential language issues
                try:
                    self.model = vosk.Model()  # type: ignore
                except Exception as e:
                    # Fallback to explicit language model if default fails
                    print(f"Warning: Default model failed: {e}")
                    # Try to load a small English model as fallback
                    self.model = vosk.Model(lang="en-us")  # type: ignore
            
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Vosk model: {e}")
        
        # Initialize audio input
        try:
            self.audio = pyaudio.PyAudio()  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Failed to initialize PyAudio: {e}")
    
    def recognize_from_microphone(self, duration: int = 5) -> Optional[str]:
        """
        Capture voice input from microphone and convert to text
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Recognized text, or None if recognition failed
        """
        if not PYAUDIO_AVAILABLE:
            return None
            
        stream = None
        try:
            # Open audio stream
            stream = self.audio.open(
                format=pyaudio.paInt16,  # type: ignore
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192
            )
            
            print("Listening... Please speak now.")
            stream.start_stream()
            
            # Record and recognize
            for i in range(0, int(16000 / 8192 * duration)):
                data = stream.read(8192)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    return result.get('text', '')
            
            # Get final result
            final_result = json.loads(self.recognizer.FinalResult())
            return final_result.get('text', '')
            
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None
        finally:
            # Clean up resources
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
    
    def close(self):
        """Release resources"""
        if hasattr(self, 'audio'):
            try:
                self.audio.terminate()
            except:
                pass

# Fallback class if dependencies are not available
class MockSpeechRecognizer:
    """Mock speech recognizer for fallback when Vosk/PyAudio not available"""
    
    def __init__(self, model_path: Optional[str] = None):
        print("Warning: Speech recognition not available. Install vosk and pyaudio for voice input.")
    
    def recognize_from_microphone(self, duration: int = 5) -> Optional[str]:
        print("Speech recognition not available.")
        return None
    
    def close(self):
        pass

# Export the appropriate class
if VOSK_AVAILABLE and PYAUDIO_AVAILABLE:
    SpeechRecognition = SpeechRecognizer
else:
    SpeechRecognition = MockSpeechRecognizer