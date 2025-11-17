import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class StudentAnalytics:
    def __init__(self, data_file="data/student_analytics.json"):
        """Initialize the student analytics system."""
        self.data_file = data_file
        self.sessions = {}
        self.interactions = []
        
    def track_interaction(self, user_message: str, assistant_response: str, session_id: Optional[str] = None):
        """Track a single interaction between student and assistant."""
        interaction = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'assistant_response': assistant_response,
            'message_length': len(user_message)
        }
        
        self.interactions.append(interaction)
        
        if session_id:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'start_time': datetime.now().isoformat(),
                    'interactions': []
                }
            self.sessions[session_id]['interactions'].append(interaction)
    
    def track_voice_interaction(self, transcription: str, response: str, session_id: Optional[str] = None):
        """Track a voice interaction."""
        self.track_interaction(transcription, response, session_id)
    
    def get_session_analytics(self, session_id: str) -> Dict:
        """Get analytics for a specific session."""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        session = self.sessions[session_id]
        interactions = session['interactions']
        
        return {
            'session_id': session_id,
            'total_interactions': len(interactions),
            'start_time': session['start_time'],
            'average_message_length': sum(i['message_length'] for i in interactions) / len(interactions) if interactions else 0
        }
    
    def get_general_analytics(self) -> Dict:
        """Get general analytics across all sessions."""
        total_sessions = len(self.sessions)
        total_interactions = len(self.interactions)
        
        return {
            'total_sessions': total_sessions,
            'total_interactions': total_interactions,
            'average_interactions_per_session': total_interactions / total_sessions if total_sessions > 0 else 0
        }
