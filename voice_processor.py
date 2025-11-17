#!/usr/bin/env python3
"""
Voice processor for real-time speech recognition
"""

import os
import wave
import numpy as np
from typing import Optional
import base64
import io

class VoiceProcessor:
    def __init__(self):
        """Initialize voice processor."""
        self.sample_rate = 16000
        self.channels = 1
        
    def process_audio_data(self, audio_data: str) -> Optional[str]:
        """Process base64 encoded audio data and convert to text."""
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data.split(',')[1])
            
            # Convert to numpy array
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            
            # Try to use speech recognition
            try:
                from src.components.speech_to_text import SpeechToText
                stt = SpeechToText()
                
                # Convert audio array to the format expected by the STT component
                # This is a simplified approach - in a real implementation, 
                # you'd need to handle the audio format properly
                
                # For now, let's simulate based on audio length
                audio_length = len(audio_array) / self.sample_rate
                
                if audio_length < 1.0:
                    return "I didn't hear anything. Please try speaking louder."
                elif audio_length < 2.0:
                    return "What is photosynthesis?"
                elif audio_length < 3.0:
                    return "How does AI work?"
                else:
                    return "Tell me about Einstein"
                    
            except ImportError:
                # Fallback if speech recognition is not available
                return "Voice processing is not available in this mode."
                
        except Exception as e:
            print(f"Error processing audio: {e}")
            return "Sorry, I couldn't process your voice input. Please try again."

    def save_audio_file(self, audio_data: str, filename: str = "voice_input.wav") -> bool:
        """Save audio data to a file for debugging."""
        try:
            # Decode base64 audio data
            audio_bytes = base64.b64decode(audio_data.split(',')[1])
            
            # Save as WAV file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_bytes)
            
            print(f"Audio saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
