# 🎓 AI Virtual Assistant for Students

An intelligent, voice-enabled virtual assistant designed specifically for students, powered by Google's Gemini AI and featuring advanced NLP, knowledge graph integration, and real-time voice processing.

## ✨ Features

### 🧠 **Intelligent Learning Assistant**
- **Gemini-Powered NLP**: Advanced natural language processing using Google's Gemini model
- **Student-Focused Responses**: Tailored explanations and learning guidance
- **Complexity Analysis**: Automatically adjusts explanations based on student level
- **Learning Gap Detection**: Identifies areas where students need more help

### 🎤 **Voice Interaction**
- **Real-time Speech Recognition**: Convert speech to text using Whisper
- **Voice Activity Detection**: Automatically detects when you start/stop speaking
- **Text-to-Speech Response**: Hear the assistant's responses aloud
- **Silence Detection**: Automatically stops recording when you pause

### 📚 **Knowledge Graph Integration**
- **Rich Educational Content**: Pre-loaded with biology, physics, computer science, and history
- **Entity Recognition**: Automatically identifies key concepts in your questions
- **Related Topic Suggestions**: Discover connections between different subjects
- **Contextual Responses**: Provides relevant information from the knowledge base

### 📊 **Learning Analytics**
- **Session Tracking**: Monitor your learning progress
- **Interaction History**: Review past conversations
- **Topic Analysis**: See what subjects you've been studying
- **Performance Insights**: Get personalized learning recommendations

### 🌐 **Web Interface**
- **Modern UI**: Clean, responsive design
- **Real-time Chat**: Instant messaging with the assistant
- **Voice Controls**: Click-to-talk functionality
- **Knowledge Search**: Search the educational database

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google API key for Gemini
- Microphone for voice features

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Virtual-Assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   ```bash
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Troubleshooting

### Microphone Issues

If you're experiencing microphone access problems, follow these steps:

1. **Test your microphone setup**
   - Open `test_microphone.html` in your browser
   - Follow the step-by-step testing process
   - This will help identify the specific issue

2. **Common solutions:**
   - **Permission denied**: Click the microphone icon in your browser's address bar and select "Allow"
   - **No microphone found**: Connect a microphone and refresh the page
   - **Microphone in use**: Close other applications using the microphone
   - **HTTPS required**: Use `https://` or `localhost` (not `http://` on external domains)

3. **Browser-specific fixes:**
   - **Chrome**: Settings → Privacy and security → Site Settings → Microphone
   - **Firefox**: Settings → Privacy & Security → Permissions → Microphone
   - **Safari**: Safari → Preferences → Websites → Microphone

4. **System-level checks:**
   - Ensure microphone is not muted in system settings
   - Check if microphone is set as default input device
   - Try a different microphone if available

### Other Common Issues

- **API Key errors**: Make sure your Google API key is set correctly
- **Port conflicts**: Change the port in `app.py` if 5000 is in use
- **Dependency issues**: Reinstall requirements with `pip install -r requirements.txt --force-reinstall`

## 📖 Usage Guide

### Text Chat
1. Type your question in the chat input
2. Press Enter or click Send
3. Get an intelligent response from the AI assistant

### Voice Interaction
1. Click the "🎤 Voice" button to start recording
2. Speak your question clearly
3. Click "⏹️ Stop" when finished
4. Hear the assistant's response

### Knowledge Search
1. Use the search bar in the sidebar
2. Search for specific topics or concepts
3. Get relevant information from the knowledge base

### Learning Analytics
- View your session statistics in the sidebar
- Track topics discussed
- Monitor your learning progress

## 🏗️ Architecture

```
AI Virtual Assistant/
├── app.py                 # Main Flask application
├── src/
│   ├── assistant_pipeline.py      # Core assistant logic
│   └── components/
│       ├── nlp_core.py           # Gemini-powered NLP
│       ├── speech_to_text.py     # Whisper speech recognition
│       ├── text_to_speech.py     # Speech synthesis
│       ├── knowledge_graph.py    # Educational knowledge base
│       ├── voice_interface.py    # Real-time voice processing
│       └── student_analytics.py  # Learning analytics
├── data/
│   └── knowledge_graph_data.json # Educational content
├── templates/
│   └── index.html               # Web interface
└── requirements.txt             # Python dependencies
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google API key for Gemini access

### Model Configuration
- **NLP Model**: `gemini-1.5-flash` (configurable in `nlp_core.py`)
- **Speech Recognition**: `openai/whisper-large-v3` (configurable in `speech_to_text.py`)
- **Text-to-Speech**: `microsoft/speecht5_tts` (configurable in `text_to_speech.py`)

## 📚 Knowledge Base

The system includes a comprehensive knowledge graph with:

- **Biology**: Photosynthesis, cellular respiration, organelles
- **Computer Science**: AI, machine learning, neural networks
- **Physics**: General relativity, famous scientists
- **History**: World War II, key historical figures

## 🎯 Example Questions

Try asking the assistant:

- "What is photosynthesis?"
- "How do neural networks work?"
- "Explain Einstein's theory of relativity"
- "What was Alan Turing's contribution to computer science?"
- "Can you help me understand cellular respiration?"

## 🔍 API Endpoints

- `GET /` - Main web interface
- `POST /api/chat` - Text-based chat
- `POST /api/voice/start` - Start voice recording
- `POST /api/voice/stop` - Stop voice recording and process
- `GET /api/analytics` - Get learning analytics
- `POST /api/knowledge/search` - Search knowledge base
- `GET /api/conversation/history` - Get chat history

## 🛠️ Development

### Adding New Knowledge
Edit `data/knowledge_graph_data.json` to add new educational content:

```json
{
  "id": "NEW001",
  "entity": "Your Topic",
  "type": "Subject Category",
  "summary": "Brief description",
  "description": "Detailed explanation",
  "properties": {
    "key_points": ["point1", "point2"]
  },
  "relationships": [
    {
      "target_id": "RELATED001",
      "relation_type": "related_to",
      "description": "How it relates"
    }
  ]
}
```

### Customizing Models
- Modify model names in component initialization
- Adjust parameters for speech recognition sensitivity
- Customize the system prompt for different use cases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini for advanced AI capabilities
- OpenAI Whisper for speech recognition
- Microsoft SpeechT5 for text-to-speech
- The open-source community for various libraries

## 🆘 Support

If you encounter any issues:

1. Check that all dependencies are installed
2. Verify your Google API key is set correctly
3. Ensure your microphone is working for voice features
4. Check the console for error messages

For additional help, please open an issue on the repository.
