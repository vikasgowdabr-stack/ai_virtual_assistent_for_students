import torch
from transformers import pipeline
import soundfile as sf
import numpy as np
import io
from typing import Optional, Union

class SpeechToText:
    def __init__(self, model_name="openai/whisper-large-v3"):
        """Initialize the speech-to-text component."""
        try:
            # Force CPU usage to avoid CUDA memory issues
            self.pipe = pipeline(
                "automatic-speech-recognition",
                model=model_name,
                device=-1  # Force CPU
            )
            print(f"✅ Speech-to-text model loaded: {model_name} (CPU)")
        except Exception as e:
            print(f"❌ Error loading speech-to-text model: {e}")
            self.pipe = None

    def transcribe(self, audio_path: str) -> Optional[str]:
        """Transcribes audio from a file path."""
        if not self.pipe:
            return "Speech-to-text model not available."
        
        try:
            audio, sample_rate = sf.read(audio_path)
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)  # Convert to mono
            
            transcript = self.pipe({"raw": audio, "sampling_rate": sample_rate})
            return transcript["text"]
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def transcribe_audio_data(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[str]:
        """Transcribes audio from raw audio data bytes."""
        if not self.pipe:
            return "Speech-to-text model not available."
        
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Normalize audio
            audio_array = audio_array.astype(np.float32) / 32768.0
            
            transcript = self.pipe({"raw": audio_array, "sampling_rate": sample_rate})
            return transcript["text"]
        except Exception as e:
            print(f"Error during audio data transcription: {e}")
            return None

    def transcribe_from_wav_bytes(self, wav_bytes: bytes) -> Optional[str]:
        """Transcribes audio from WAV format bytes."""
        if not self.pipe:
            return "Speech-to-text model not available."
        
        try:
            # Read WAV data using soundfile
            audio, sample_rate = sf.read(io.BytesIO(wav_bytes))
            
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)  # Convert to mono
            
            transcript = self.pipe({"raw": audio, "sampling_rate": sample_rate})
            return transcript["text"]
        except Exception as e:
            print(f"Error during WAV transcription: {e}")
            return None

    def is_model_available(self) -> bool:
        """Check if the speech-to-text model is available."""
        return self.pipe is not None

    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self.pipe:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.pipe.model.name_or_path if hasattr(self.pipe, 'model') else "unknown",
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }