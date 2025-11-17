from transformers import pipeline
import soundfile as sf
from datasets import load_dataset
import numpy as np
from typing import Optional, Tuple
import os

class TextToSpeech:
    def __init__(self, model_name="microsoft/speecht5_tts"):
        """Initialize the text-to-speech component."""
        try:
            # Force CPU usage to avoid CUDA memory issues
            self.synthesiser = pipeline("text-to-speech", model_name, device=-1)
            # Use a simpler approach for speaker embeddings
            self.speaker_embedding = None
            self.last_audio_path = None
            print(f"✅ Text-to-speech model loaded: {model_name} (CPU)")
        except Exception as e:
            print(f"❌ Error loading text-to-speech model: {e}")
            self.synthesiser = None
            self.speaker_embedding = None

    def speak(self, text: str, output_path: str = "output.wav") -> Optional[str]:
        """Converts text to speech and saves it to a file."""
        if not self.synthesiser:
            return None
        
        try:
            # Generate speech without speaker embeddings
            speech = self.synthesiser(text)
            sf.write(output_path, speech["audio"], samplerate=speech["sampling_rate"])
            self.last_audio_path = output_path
            print(f"Speech saved to {output_path}")
            return output_path
        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")
            return None

    def speak_to_audio(self, text: str) -> Optional[bytes]:
        """Converts text to speech and returns audio data as bytes."""
        if not self.synthesiser:
            return None
        
        try:
            speech = self.synthesiser(text)
            
            # Convert audio to bytes
            audio_bytes = self._audio_to_bytes(speech["audio"], speech["sampling_rate"])
            return audio_bytes
        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")
            return None

    def speak_to_array(self, text: str) -> Optional[Tuple[np.ndarray, int]]:
        """Converts text to speech and returns audio array and sample rate."""
        if not self.synthesiser:
            return None
        
        try:
            speech = self.synthesiser(text)
            return speech["audio"], speech["sampling_rate"]
        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")
            return None

    def _audio_to_bytes(self, audio_array: np.ndarray, sample_rate: int) -> bytes:
        """Convert audio array to WAV bytes."""
        try:
            # Create a temporary file-like object
            import io
            buffer = io.BytesIO()
            
            # Write audio to buffer
            sf.write(buffer, audio_array, sample_rate, format='WAV')
            buffer.seek(0)
            
            return buffer.getvalue()
        except Exception as e:
            print(f"Error converting audio to bytes: {e}")
            return b""

    def get_last_audio_path(self) -> Optional[str]:
        """Get the path of the last generated audio file."""
        return self.last_audio_path

    def is_model_available(self) -> bool:
        """Check if the text-to-speech model is available."""
        return self.synthesiser is not None

    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self.synthesiser:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.synthesiser.model.name_or_path if hasattr(self.synthesiser, 'model') else "unknown",
            "speaker_embedding_available": self.speaker_embedding is not None
        }

    def cleanup_audio_files(self, keep_recent: int = 5):
        """Clean up old audio files, keeping only the most recent ones."""
        if not self.last_audio_path:
            return
        
        try:
            output_dir = os.path.dirname(self.last_audio_path)
            if not output_dir:
                output_dir = "."
            
            # Find all audio files in the directory
            audio_files = [f for f in os.listdir(output_dir) if f.endswith('.wav')]
            
            if len(audio_files) > keep_recent:
                # Sort by modification time and remove old files
                audio_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
                
                for old_file in audio_files[:-keep_recent]:
                    try:
                        os.remove(os.path.join(output_dir, old_file))
                        print(f"Cleaned up old audio file: {old_file}")
                    except Exception as e:
                        print(f"Error removing file {old_file}: {e}")
        except Exception as e:
            print(f"Error during audio cleanup: {e}")