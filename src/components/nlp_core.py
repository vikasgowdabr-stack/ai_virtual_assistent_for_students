import google.generativeai as genai
import os
from typing import List, Dict, Optional
import json

class NLPCore:
    def __init__(self, model_name="gemini-1.5-flash"):
        """Initialize the NLP core with Gemini model."""
        # Set up Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            print("Please set your Google API key to use Gemini features.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        
        # Student-focused system prompt
        self.system_prompt = """You are an intelligent, friendly, and knowledgeable AI tutor designed specifically for students. Your role is to:

1. **Provide Clear Explanations**: Break down complex concepts into simple, understandable terms
2. **Encourage Critical Thinking**: Ask follow-up questions to help students think deeper
3. **Adapt to Learning Level**: Adjust your explanations based on the student's apparent knowledge level
4. **Be Patient and Supportive**: Create a safe learning environment where students feel comfortable asking questions
5. **Provide Real-World Examples**: Connect abstract concepts to practical applications
6. **Encourage Active Learning**: Suggest activities, experiments, or further reading when appropriate

Always maintain a positive, encouraging tone and remember that learning is a journey. If you're unsure about something, be honest about it and suggest where the student might find more information."""

    def generate_response(self, question: str, context: Optional[str] = None, 
                         conversation_history: Optional[List[Dict]] = None) -> str:
        """Generate a response to a student's question using Gemini."""
        if not self.model:
            return "I'm sorry, but I'm not properly configured to respond right now. Please check your API key setup."
        
        try:
            # Build the conversation context
            messages = [{"role": "user", "parts": [self.system_prompt]}]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    if msg.get('user'):
                        messages.append({"role": "user", "parts": [msg['user']]})
                    if msg.get('assistant'):
                        messages.append({"role": "model", "parts": [msg['assistant']]})
            
            # Add current context if available
            if context:
                context_prompt = f"Use this additional information to help answer the question: {context}"
                messages.append({"role": "user", "parts": [context_prompt]})
            
            # Add the current question
            messages.append({"role": "user", "parts": [question]})
            
            # Generate response
            response = self.model.generate_content(messages)
            
            return response.text
            
        except Exception as e:
            print(f"Error generating NLP response: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."

    def analyze_question_complexity(self, question: str) -> Dict:
        """Analyze the complexity level of a student's question."""
        if not self.model:
            return {"complexity": "unknown", "confidence": 0.0}
        
        try:
            analysis_prompt = f"""
            Analyze the complexity of this student question and provide a structured response:
            Question: "{question}"
            
            Please respond with a JSON object containing:
            - complexity_level: "beginner", "intermediate", or "advanced"
            - subject_area: the main academic subject (e.g., "biology", "mathematics", "history")
            - key_concepts: list of main concepts mentioned
            - confidence_score: 0.0 to 1.0
            """
            
            response = self.model.generate_content(analysis_prompt)
            
            # Try to parse JSON response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback analysis
                return {
                    "complexity_level": "intermediate",
                    "subject_area": "general",
                    "key_concepts": [],
                    "confidence_score": 0.5
                }
                
        except Exception as e:
            print(f"Error analyzing question complexity: {e}")
            return {"complexity": "unknown", "confidence": 0.0}

    def generate_follow_up_questions(self, topic: str, student_level: str = "intermediate") -> List[str]:
        """Generate follow-up questions to encourage deeper learning."""
        if not self.model:
            return ["What aspects of this topic would you like to explore further?"]
        
        try:
            prompt = f"""
            Generate 3-5 thoughtful follow-up questions about "{topic}" for a {student_level} level student.
            The questions should:
            - Encourage critical thinking
            - Connect to real-world applications
            - Build upon the student's current knowledge
            - Be open-ended and engaging
            
            Return only the questions, one per line.
            """
            
            response = self.model.generate_content(prompt)
            questions = [q.strip() for q in response.text.split('\n') if q.strip()]
            
            return questions[:5]  # Limit to 5 questions
            
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            return ["What aspects of this topic would you like to explore further?"]

    def summarize_conversation(self, conversation_history: List[Dict]) -> str:
        """Summarize a conversation session for learning insights."""
        if not self.model or not conversation_history:
            return "No conversation to summarize."
        
        try:
            # Format conversation for summarization
            conversation_text = ""
            for msg in conversation_history:
                if msg.get('user'):
                    conversation_text += f"Student: {msg['user']}\n"
                if msg.get('assistant'):
                    conversation_text += f"Tutor: {msg['assistant']}\n"
            
            summary_prompt = f"""
            Summarize this tutoring conversation and provide learning insights:
            
            {conversation_text}
            
            Please provide:
            1. Main topics discussed
            2. Key learning points
            3. Suggested next steps for the student
            4. Areas that might need more attention
            """
            
            response = self.model.generate_content(summary_prompt)
            return response.text
            
        except Exception as e:
            print(f"Error summarizing conversation: {e}")
            return "Unable to generate conversation summary."

    def detect_learning_gaps(self, question: str, student_responses: List[str]) -> List[str]:
        """Detect potential learning gaps based on student questions and responses."""
        if not self.model:
            return []
        
        try:
            analysis_prompt = f"""
            Analyze this student's learning pattern and identify potential gaps:
            
            Recent question: "{question}"
            Previous responses: {student_responses}
            
            Identify potential learning gaps or misconceptions. Return as a list of specific areas that need attention.
            """
            
            response = self.model.generate_content(analysis_prompt)
            gaps = [gap.strip() for gap in response.text.split('\n') if gap.strip()]
            
            return gaps[:5]  # Limit to 5 gaps
            
        except Exception as e:
            print(f"Error detecting learning gaps: {e}")
            return []