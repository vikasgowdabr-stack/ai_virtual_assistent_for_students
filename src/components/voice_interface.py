import pyaudio
import wave
import numpy as np
import threading
import time
import webrtcvad
from typing import Optional, List
import io

class VoiceInterface:
    def __init__(self, sample_rate=16000, chunk_size=1024, channels=1):
        """Initialize the voice interface for real-time audio processing."""
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.format = pyaudio.paInt16
        
        # Audio processing
        self.audio = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        
        # Recording state
        self.is_recording = False
        self.recording_thread = None
        self.audio_frames = []
        self.silence_threshold = 1.0  # seconds of silence to stop recording
        self.last_speech_time = 0
        
    def start_recording(self):
        """Start recording audio from the microphone."""
        if self.is_recording:
            print("Already recording...")
            return
        
        self.is_recording = True
        self.audio_frames = []
        self.last_speech_time = time.time()
        
        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        
        print("🎤 Started recording...")
    
    def stop_recording(self) -> Optional[bytes]:
        """Stop recording and return the audio data."""
        if not self.is_recording:
            print("Not currently recording...")
            return None
        
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if self.audio_frames:
            # Combine all audio frames
            audio_data = b''.join(self.audio_frames)
            print(f"🎤 Stopped recording. Captured {len(audio_data)} bytes of audio.")
            return audio_data
        else:
            print("No audio data captured.")
            return None
    
    def _record_audio(self):
        """Internal method to record audio in a separate thread."""
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            consecutive_silence_chunks = 0
            silence_chunks_threshold = int(self.silence_threshold * self.sample_rate / self.chunk_size)
            
            while self.is_recording:
                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    self.audio_frames.append(data)
                    
                    # Voice Activity Detection
                    if self._is_speech(data):
                        consecutive_silence_chunks = 0
                        self.last_speech_time = time.time()
                    else:
                        consecutive_silence_chunks += 1
                    
                    # Stop recording if silence threshold is reached
                    if consecutive_silence_chunks >= silence_chunks_threshold:
                        print("🔇 Silence detected, stopping recording...")
                        break
                        
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Error in audio recording: {e}")
    
    def _is_speech(self, audio_chunk: bytes) -> bool:
        """Detect if an audio chunk contains speech."""
        try:
            return self.vad.is_speech(audio_chunk, self.sample_rate)
        except Exception:
            return True  # Default to speech if VAD fails
    
    def save_audio_to_file(self, audio_data: bytes, filename: str = "recorded_audio.wav"):
        """Save recorded audio data to a WAV file."""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data)
            print(f"Audio saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving audio: {e}")
            return None
    
    def get_audio_duration(self, audio_data: bytes) -> float:
        """Calculate the duration of audio data in seconds."""
        if not audio_data:
            return 0.0
        
        # Calculate duration based on audio format
        bytes_per_sample = 2  # 16-bit audio
        total_samples = len(audio_data) // bytes_per_sample
        duration = total_samples / self.sample_rate
        
        return duration
    
    def is_recording_active(self) -> bool:
        """Check if recording is currently active."""
        return self.is_recording
    
    def get_recording_stats(self) -> dict:
        """Get statistics about the current recording session."""
        if not self.audio_frames:
            return {"duration": 0, "frames": 0, "bytes": 0}
        
        total_bytes = sum(len(frame) for frame in self.audio_frames)
        duration = self.get_audio_duration(b''.join(self.audio_frames))
        
        return {
            "duration": duration,
            "frames": len(self.audio_frames),
            "bytes": total_bytes,
            "is_active": self.is_recording
        }
    
    def cleanup(self):
        """Clean up audio resources."""
        if self.is_recording:
            self.stop_recording()
        
        if hasattr(self, 'audio') and self.audio:
            try:
                self.audio.terminate()
            except:
                pass
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()
