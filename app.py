import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import threading
import time
from src.assistant_pipeline import AssistantPipeline
from src.components.voice_interface import VoiceInterface
from src.components.student_analytics import StudentAnalytics
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

# Initialize the assistant pipeline
assistant = AssistantPipeline()
voice_interface = VoiceInterface()
analytics = StudentAnalytics()

# Global state for conversation history
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
        
        # Process the message through the assistant pipeline
        response = assistant.process_text_message(user_message)
        
        # Add to conversation history
        conversation_history.append({
            'user': user_message,
            'assistant': response,
            'timestamp': time.time()
        })
        
        # Track analytics
        analytics.track_interaction(user_message, response, session_id)
        
        return jsonify({
            'response': response,
            'conversation_id': len(conversation_history)
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
        
        # Start voice recording
        voice_interface.start_recording()
        
        return jsonify({'status': 'recording_started'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_session():
    """Stop voice recording and process the audio."""
    try:
        # Stop recording and get audio data
        audio_data = voice_interface.stop_recording()
        
        if audio_data:
            # Process through speech-to-text
            question_text = assistant.stt.transcribe_audio_data(audio_data)
            
            if question_text:
                # Process through the full pipeline
                response = assistant.process_text_message(question_text)
                
                # Generate speech response
                audio_response = assistant.tts.speak_to_audio(response)
                
                # Track analytics
                analytics.track_voice_interaction(question_text, response, student_session.get('session_id'))
                
                return jsonify({
                    'transcription': question_text,
                    'response': response,
                    'audio_url': '/api/audio/response'
                })
            else:
                return jsonify({'error': 'Could not transcribe audio'}), 400
        else:
            return jsonify({'error': 'No audio data received'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/response')
def get_audio_response():
    """Serve the generated audio response."""
    try:
        audio_path = assistant.tts.get_last_audio_path()
        if audio_path and os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get student analytics and progress."""
    try:
        session_id = request.args.get('session_id')
        if session_id:
            return jsonify(analytics.get_session_analytics(session_id))
        else:
            return jsonify(analytics.get_general_analytics())
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
        
        # Search knowledge graph
        results = assistant.kg.search_knowledge(query)
        
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
    print("🚀 Starting AI Virtual Assistant for Students...")
    
    # Check if components loaded successfully
    if assistant.nlp.model is None:
        print("⚠️  Warning: Gemini NLP not available (no API key)")
    else:
        print("🧠 Gemini-powered NLP core initialized")
    
    if assistant.stt.pipe is None:
        print("⚠️  Warning: Speech-to-text not available")
    else:
        print("🎤 Voice interface ready")
    
    if assistant.tts.synthesiser is None:
        print("⚠️  Warning: Text-to-speech not available")
    else:
        print("🔊 Speech synthesis ready")
    
    if assistant.kg.kg_data:
        print(f"📚 Knowledge Graph loaded with {len(assistant.kg.kg_data)} entities")
    else:
        print("⚠️  Warning: Knowledge graph not available")
    
    print("📊 Analytics tracking enabled")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("\n🌐 Starting web server...")
    print("The application will be available at: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=8080)

if __name__ == "__main__":
    print("🚀 Starting AI Virtual Assistant...")
    
    # Check if HTTPS is requested
    use_https = os.getenv('USE_HTTPS', 'false').lower() == 'true'
    
    if use_https:
        cert_path, key_path = create_ssl_context()
        if cert_path and key_path:
            print("🔒 Starting with HTTPS...")
            print("The application will be available at: https://localhost:5000")
            print("Note: You may see a security warning - this is normal for self-signed certificates.")
            print("Click 'Advanced' and 'Proceed to localhost' to continue.")
            app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=(cert_path, key_path))
        else:
            print("⚠️  HTTPS not available, falling back to HTTP...")
            print("The application will be available at: http://localhost:5000")
            app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        print("🌐 Starting with HTTP...")
        print("The application will be available at: http://localhost:5000")
        print("For microphone access from external domains, set USE_HTTPS=true")
        app.run(debug=False, host='0.0.0.0', port=5000)


