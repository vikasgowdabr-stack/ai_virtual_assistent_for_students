import os
from typing import Dict, Any

class Config:
    """Configuration settings for the AI Virtual Assistant."""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # Model Settings
    NLP_MODEL = "gemini-1.5-flash"
    SPEECH_TO_TEXT_MODEL = "openai/whisper-large-v3"
    TEXT_TO_SPEECH_MODEL = "microsoft/speecht5_tts"
    NER_MODEL = "dslim/bert-base-NER"
    
    # Audio Settings
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    CHANNELS = 1
    SILENCE_THRESHOLD = 1.0  # seconds
    
    # File Paths
    KNOWLEDGE_GRAPH_DATA = "data/knowledge_graph_data.json"
    ANALYTICS_DATA = "data/student_analytics.json"
    
    # Web Server
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True
    
    # Session Settings
    MAX_CONVERSATION_HISTORY = 50
    SESSION_TIMEOUT = 3600  # 1 hour
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration and return status."""
        status = {
            'google_api_key': bool(cls.GOOGLE_API_KEY),
            'knowledge_graph': os.path.exists(cls.KNOWLEDGE_GRAPH_DATA),
            'models': {
                'nlp': cls.NLP_MODEL,
                'stt': cls.SPEECH_TO_TEXT_MODEL,
                'tts': TEXT_TO_SPEECH_MODEL,
                'ner': cls.NER_MODEL
            }
        }
        
        if not status['google_api_key']:
            print("⚠️  Warning: GOOGLE_API_KEY not set. Gemini features will be disabled.")
        
        if not status['knowledge_graph']:
            print("⚠️  Warning: Knowledge graph data file not found.")
        
        return status
