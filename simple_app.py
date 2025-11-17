import os
import time
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import ssl
import tempfile

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
conversation_history = []
student_session = {
    "session_id": None,
    "topics_discussed": [],
    "questions_asked": 0,
    "start_time": None
}

@app.route('/')
def index():
    """Main interface for the AI Virtual Assistant."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text-based chat interactions."""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Update session
        if session_id:
            student_session['session_id'] = session_id
            if not student_session['start_time']:
                student_session['start_time'] = time.time()
            student_session['questions_asked'] += 1
        
        # Simple response logic
        response = generate_simple_response(user_message)
        
        # Add to conversation history
        conversation_history.append({
            'user': user_message,
            'assistant': response,
            'timestamp': time.time()
        })
        
        return jsonify({
            'response': response,
            'conversation_id': len(conversation_history)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_simple_response(message):
    """Generate a response using Gemini AI if available, otherwise use simple keywords."""
    try:
        # Try to use Gemini AI
        import google.generativeai as genai
        import os
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Create a student-focused prompt
            prompt = f"""You are an intelligent, friendly AI tutor for students. Answer this question: {message}
            
            Keep your response concise (2-3 sentences maximum), helpful, and encouraging. Be direct and to the point."""
            
            response = model.generate_content(prompt)
            return response.text
        else:
            raise Exception("No API key found")
            
    except Exception as e:
        # Fallback to simple keyword responses
        message_lower = message.lower()
        
        if 'hello' in message_lower or 'hi' in message_lower:
            return "Hello! I'm your AI learning assistant. How can I help you today?"
        
        elif 'photosynthesis' in message_lower:
            return "Photosynthesis is the process by which plants convert light energy into chemical energy. It occurs in chloroplasts and produces glucose and oxygen from carbon dioxide and water."
        
        elif 'ai' in message_lower or 'artificial intelligence' in message_lower:
            return "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes machine learning, natural language processing, and computer vision."
        
        elif 'einstein' in message_lower:
            return "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity. He's considered one of the most influential scientists of the 20th century."
        
        elif 'neural network' in message_lower:
            return "Neural networks are computing systems inspired by biological neural networks. They're used in machine learning for pattern recognition and decision making."
        
        elif 'help' in message_lower:
            return "I can help you learn about various topics including biology, physics, computer science, and history. Just ask me any question!"
        
        else:
            return f"I received your message: '{message}'. I'm here to help you learn! Ask me about any subject."

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get student analytics and progress."""
    try:
        session_id = request.args.get('session_id')
        if session_id:
            return jsonify({
                'session_id': session_id,
                'total_interactions': len(conversation_history),
                'start_time': student_session.get('start_time'),
                'average_message_length': 50  # Placeholder
            })
        else:
            return jsonify({
                'total_sessions': 1,
                'total_interactions': len(conversation_history),
                'average_interactions_per_session': len(conversation_history)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge/search', methods=['POST'])
def search_knowledge():
    """Search the knowledge graph for specific topics."""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Simple search results
        results = []
        query_lower = query.lower()
        
        if 'photosynthesis' in query_lower:
            results.append({
                'item': {
                    'entity': 'Photosynthesis',
                    'summary': 'The process by which plants convert light energy into chemical energy.'
                },
                'relevance_score': 3
            })
        
        if 'ai' in query_lower or 'artificial intelligence' in query_lower:
            results.append({
                'item': {
                    'entity': 'Artificial Intelligence',
                    'summary': 'The simulation of human intelligence in machines.'
                },
                'relevance_score': 3
            })
        
        return jsonify({
            'query': query,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get conversation history."""
    try:
        limit = request.args.get('limit', 10, type=int)
        return jsonify({
            'history': conversation_history[-limit:],
            'total_messages': len(conversation_history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/start', methods=['POST'])
def start_voice_session():
    """Start a voice interaction session."""
    try:
        session_id = request.json.get('session_id')
        if session_id:
            student_session['session_id'] = session_id
            student_session['start_time'] = time.time()
        
        return jsonify({'status': 'recording_started'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_session():
    """Stop voice recording and process the audio."""
    try:
        data = request.json
        audio_data = data.get('audio_data')
        
        if not audio_data:
            return jsonify({'error': 'No audio data received'}), 400
        
        # Process the actual audio data
        try:
            from voice_processor import VoiceProcessor
            processor = VoiceProcessor()
            
            # Process the audio and get transcription
            transcription = processor.process_audio_data(audio_data)
            
            if transcription:
                # Generate response using the same logic as text chat
                response = generate_simple_response(transcription)
                
                return jsonify({
                    'transcription': transcription,
                    'response': response,
                    'audio_url': None
                })
            else:
                return jsonify({
                    'transcription': 'Could not understand audio',
                    'response': 'I couldn\'t understand what you said. Please try speaking more clearly.',
                    'audio_url': None
                })
                
        except ImportError:
            # Fallback if voice processor is not available
            return jsonify({
                'transcription': 'Voice input received',
                'response': 'I heard your voice! For full voice processing, please run the complete application.',
                'audio_url': None
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_ssl_context():
    """Create a self-signed SSL certificate for HTTPS."""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        import ipaddress
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "AI Tutor"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Create temporary files for certificate and key
        cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.crt')
        key_file = tempfile.NamedTemporaryFile(delete=False, suffix='.key')
        
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
        cert_file.close()
        key_file.close()
        
        return cert_file.name, key_file.name
        
    except ImportError:
        print("⚠️  cryptography library not installed. HTTPS not available.")
        print("Install with: pip install cryptography")
        return None, None

def main():
    """Main function to run the Flask application."""
    print("🚀 Starting Simple AI Virtual Assistant...")
    print("📚 Basic knowledge responses available")
    print("🌐 Starting web server...")
    
    # Check if HTTPS is requested
    use_https = os.getenv('USE_HTTPS', 'false').lower() == 'true'
    
    if use_https:
        cert_path, key_path = create_ssl_context()
        if cert_path and key_path:
            print("🔒 Starting with HTTPS...")
            print("The application will be available at: https://localhost:8080")
            print("Note: You may see a security warning - this is normal for self-signed certificates.")
            print("Click 'Advanced' and 'Proceed to localhost' to continue.")
            app.run(debug=False, host='0.0.0.0', port=8080, ssl_context=(cert_path, key_path))
        else:
            print("⚠️  HTTPS not available, falling back to HTTP...")
            print("The application will be available at: http://localhost:8080")
            app.run(debug=False, host='0.0.0.0', port=8080)
    else:
        print("The application will be available at: http://localhost:8080")
        print("For microphone access from external domains, set USE_HTTPS=true")
        app.run(debug=False, host='0.0.0.0', port=8080)
    
    print("Press Ctrl+C to stop the server")
    
    # Create templates directory if it doesn't exist
    import os
    os.makedirs('templates', exist_ok=True)

if __name__ == "__main__":
    main()
