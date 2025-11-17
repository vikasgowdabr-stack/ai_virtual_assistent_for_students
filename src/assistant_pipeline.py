from .components.speech_to_text import SpeechToText
from .components.nlp_core import NLPCore
from .components.knowledge_graph import KnowledgeGraph
from .components.text_to_speech import TextToSpeech
import time
from typing import List, Dict, Optional

class AssistantPipeline:
    def __init__(self):
        print("Initializing assistant components...")
        self.stt = SpeechToText()
        self.nlp = NLPCore()
        self.kg = KnowledgeGraph()
        self.tts = TextToSpeech()
        self.conversation_history = []
        print("Initialization complete.")

    def run(self, audio_input_path):
        """Runs the full virtual assistant pipeline with audio input."""
        # 1. Speech-to-Text
        print("\n[1/4] Transcribing audio...")
        question_text = self.stt.transcribe(audio_input_path)
        if not question_text:
            print("Could not transcribe audio.")
            return
        print(f"User said: {question_text}")

        # Process the question through the pipeline
        response = self.process_text_message(question_text)
        
        # 4. Text-to-Speech
        print("\n[4/4] Synthesizing speech...")
        self.tts.speak(response)
        
        return response

    def process_text_message(self, question_text: str, context: Optional[str] = None) -> str:
        """Process a text message through the assistant pipeline."""
        try:
            # 2. Knowledge Graph Integration (RAG)
            print("\n[2/4] Analyzing query and retrieving knowledge...")
            entities = self.kg.extract_entities(question_text)
            kg_context = self.kg.query_knowledge_base(entities)
            
            # Combine context sources
            full_context = context
            if kg_context:
                full_context = f"{context + ' ' if context else ''}{kg_context}"
                print(f"Retrieved context: {kg_context}")
            else:
                print("No specific knowledge found, relying on general knowledge.")

            # 3. Core NLP with Gemini
            print("\n[3/4] Generating response...")
            response_text = self.nlp.generate_response(
                question_text, 
                context=full_context,
                conversation_history=self.conversation_history
            )
            print(f"Assistant's response: {response_text}")

            # Update conversation history
            self.conversation_history.append({
                'user': question_text,
                'assistant': response_text,
                'timestamp': time.time(),
                'entities': entities,
                'context_used': bool(kg_context)
            })

            return response_text
            
        except Exception as e:
            print(f"Error in processing text message: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."

    def analyze_question(self, question: str) -> Dict:
        """Analyze a question for complexity and learning insights."""
        try:
            # Get question complexity analysis
            complexity_analysis = self.nlp.analyze_question_complexity(question)
            
            # Extract entities for topic identification
            entities = self.kg.extract_entities(question)
            
            # Get knowledge graph context
            kg_context = self.kg.query_knowledge_base(entities)
            
            return {
                'complexity': complexity_analysis,
                'entities': entities,
                'has_knowledge_context': bool(kg_context),
                'suggested_topics': self.kg.get_related_topics(entities) if entities else []
            }
        except Exception as e:
            print(f"Error analyzing question: {e}")
            return {}

    def get_learning_recommendations(self, question: str) -> Dict:
        """Get personalized learning recommendations based on the question."""
        try:
            # Analyze the question
            analysis = self.analyze_question(question)
            
            # Generate follow-up questions
            topic = analysis.get('entities', ['general learning'])[0] if analysis.get('entities') else 'general learning'
            complexity_level = analysis.get('complexity', {}).get('complexity_level', 'intermediate')
            
            follow_up_questions = self.nlp.generate_follow_up_questions(topic, complexity_level)
            
            # Get related knowledge graph entries
            related_content = []
            if analysis.get('entities'):
                related_content = self.kg.get_related_content(analysis['entities'])
            
            return {
                'follow_up_questions': follow_up_questions,
                'related_content': related_content,
                'complexity_level': complexity_level,
                'suggested_activities': self._generate_learning_activities(topic, complexity_level)
            }
        except Exception as e:
            print(f"Error getting learning recommendations: {e}")
            return {}

    def _generate_learning_activities(self, topic: str, level: str) -> List[str]:
        """Generate suggested learning activities for a topic and level."""
        activities = {
            'beginner': [
                f"Watch an introductory video about {topic}",
                f"Read a simple explanation of {topic}",
                f"Create flashcards for key {topic} terms",
                f"Draw a simple diagram of {topic}"
            ],
            'intermediate': [
                f"Research real-world applications of {topic}",
                f"Compare different aspects of {topic}",
                f"Create a mind map connecting {topic} to related concepts",
                f"Write a summary explaining {topic} to someone else"
            ],
            'advanced': [
                f"Analyze current research on {topic}",
                f"Create a detailed presentation about {topic}",
                f"Write a critical analysis of {topic}",
                f"Design an experiment related to {topic}"
            ]
        }
        
        return activities.get(level, activities['intermediate'])

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation session."""
        if not self.conversation_history:
            return "No conversation to summarize."
        
        return self.nlp.summarize_conversation(self.conversation_history)

    def detect_learning_gaps(self) -> List[str]:
        """Detect learning gaps from the conversation history."""
        if not self.conversation_history:
            return []
        
        # Extract student questions
        student_questions = [msg['user'] for msg in self.conversation_history if msg.get('user')]
        
        if not student_questions:
            return []
        
        # Use the most recent question for gap analysis
        recent_question = student_questions[-1]
        previous_responses = student_questions[:-1] if len(student_questions) > 1 else []
        
        return self.nlp.detect_learning_gaps(recent_question, previous_responses)

    def get_session_insights(self) -> Dict:
        """Get comprehensive insights about the current learning session."""
        try:
            return {
                'total_interactions': len(self.conversation_history),
                'topics_discussed': self._extract_topics_discussed(),
                'complexity_progression': self._analyze_complexity_progression(),
                'knowledge_gaps': self.detect_learning_gaps(),
                'conversation_summary': self.get_conversation_summary(),
                'session_duration': self._calculate_session_duration(),
                'learning_recommendations': self._generate_session_recommendations()
            }
        except Exception as e:
            print(f"Error getting session insights: {e}")
            return {}

    def _extract_topics_discussed(self) -> List[str]:
        """Extract main topics discussed in the session."""
        topics = set()
        for msg in self.conversation_history:
            if msg.get('entities'):
                topics.update(msg['entities'])
        return list(topics)

    def _analyze_complexity_progression(self) -> Dict:
        """Analyze how question complexity has changed during the session."""
        if len(self.conversation_history) < 2:
            return {'trend': 'insufficient_data'}
        
        complexities = []
        for msg in self.conversation_history:
            if msg.get('user'):
                analysis = self.nlp.analyze_question_complexity(msg['user'])
                complexities.append(analysis.get('complexity_level', 'intermediate'))
        
        if len(complexities) < 2:
            return {'trend': 'insufficient_data'}
        
        # Simple trend analysis
        if complexities[-1] == 'advanced' and complexities[0] == 'beginner':
            trend = 'increasing'
        elif complexities[-1] == 'beginner' and complexities[0] == 'advanced':
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'complexity_levels': complexities,
            'average_complexity': max(set(complexities), key=complexities.count)
        }

    def _calculate_session_duration(self) -> float:
        """Calculate the duration of the current session in minutes."""
        if not self.conversation_history:
            return 0.0
        
        start_time = self.conversation_history[0]['timestamp']
        end_time = self.conversation_history[-1]['timestamp']
        
        return (end_time - start_time) / 60.0  # Convert to minutes

    def _generate_session_recommendations(self) -> List[str]:
        """Generate recommendations based on the session analysis."""
        insights = self.get_session_insights()
        recommendations = []
        
        # Based on session duration
        duration = insights.get('session_duration', 0)
        if duration > 60:  # More than 1 hour
            recommendations.append("Consider taking a short break to maintain focus.")
        
        # Based on complexity progression
        complexity_trend = insights.get('complexity_progression', {}).get('trend', 'stable')
        if complexity_trend == 'increasing':
            recommendations.append("Great progress! You're tackling more complex topics.")
        elif complexity_trend == 'decreasing':
            recommendations.append("Consider revisiting foundational concepts to strengthen your understanding.")
        
        # Based on knowledge gaps
        gaps = insights.get('knowledge_gaps', [])
        if gaps:
            recommendations.append(f"Focus on these areas: {', '.join(gaps[:3])}")
        
        return recommendations