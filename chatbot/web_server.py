from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
import threading
import time
import random
from datetime import datetime

# Import chatbot functions
try:
    from chatbot3 import enhanced_match_intent, generate_response, initialize_chatbot, load_intents
    print("Successfully imported chatbot3 functions")
except ImportError as e:
    print(f"Error importing chatbot3: {e}")
    # Fallback functions
    def enhanced_match_intent(text, intents):
        # Try to match with available intents
        if intents and 'intents' in intents:
            text_lower = text.lower()
            for intent in intents['intents']:
                for pattern in intent.get('patterns', []):
                    if pattern.lower() in text_lower:
                        return random.choice(intent.get('responses', ['I understand.']))
        return None  # Return None instead of error message
    
    def generate_response(chatbot, tokenizer, text, history):
        # Simple fallback responses
        responses = [
            "That's interesting! Tell me more.",
            "I understand. How can I help you?",
            "That's a good point. What else would you like to know?",
            "I'm listening. Please continue.",
            "That's fascinating! Can you elaborate?"
        ]
        return random.choice(responses)
    
    def initialize_chatbot():
        return None, None
    
    def load_intents():
        # Return some basic intents if file loading fails
        return {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
                    "responses": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Greetings! How are you doing?"]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "assist", "support", "what can you do"],
                    "responses": ["I'm here to help! What do you need assistance with?", "I'd be happy to help you. What's on your mind?", "I'm ready to assist. What can I do for you?"]
                },
                {
                    "tag": "how_are_you",
                    "patterns": ["how are you", "how do you do", "are you okay"],
                    "responses": ["I'm doing well, thank you! How are you?", "I'm great! How can I help you today?", "I'm doing fine. What about you?"]
                }
            ]
        }

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
CORS(app)

# Global variables for chatbot state
chatbot_instance = None
tokenizer_instance = None
intents_data = None
conversation_history = {}

def initialize_chatbot_globals():
    """Initialize chatbot components"""
    global chatbot_instance, tokenizer_instance, intents_data
    
    try:
        # Load intents
        intents_data = load_intents()
        
        # Initialize chatbot
        chatbot_instance, tokenizer_instance = initialize_chatbot()
        
        print("Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        return False

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Initialize session history if not exists
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Try to match with intents first
        response = None
        if intents_data:
            print(f"Trying intent matching for: {user_message}")
            response = enhanced_match_intent(user_message, intents_data)
            if response:
                print(f"Intent match found: {response}")
            else:
                print("No intent match found")
        
        # If no intent match, use transformer model
        if not response and chatbot_instance and tokenizer_instance:
            try:
                print("Trying transformer model...")
                response = generate_response(
                    chatbot_instance, 
                    tokenizer_instance, 
                    user_message, 
                    conversation_history[session_id]
                )
                if response:
                    print(f"Transformer response: {response}")
                else:
                    print("Transformer model returned empty response")
            except Exception as e:
                print(f"Error generating response: {e}")
                response = "I'm having trouble processing that right now. Please try again."
        elif not response:
            print("No chatbot instance available, using fallback")
        
        # Fallback response with more variety and context awareness
        if not response:
            # Get conversation history for context
            history = conversation_history[session_id]
            recent_messages = history[-4:] if len(history) >= 4 else history
            
            # More diverse fallback responses based on conversation context
            if len(recent_messages) == 0:
                responses = [
                    "Hello! I'm here to help. What would you like to talk about?",
                    "Hi there! How can I assist you today?",
                    "Greetings! What's on your mind?",
                    "Hello! I'm ready to chat. What would you like to discuss?"
                ]
            elif any(word in user_message.lower() for word in ['how', 'what', 'why', 'when', 'where', 'who']):
                responses = [
                    "That's a great question! Let me think about that.",
                    "I'd be happy to help with that. Could you provide more details?",
                    "That's interesting! Can you tell me more about what you're looking for?",
                    "I want to make sure I understand correctly. Could you elaborate?",
                    "That's a thoughtful question. What specific aspect interests you most?"
                ]
            elif any(word in user_message.lower() for word in ['help', 'assist', 'support']):
                responses = [
                    "I'm here to help! What specific assistance do you need?",
                    "I'd be glad to assist you. What can I do for you?",
                    "I'm ready to help! What would you like to know?",
                    "I'm here to support you. What do you need help with?"
                ]
            else:
                responses = [
                    "That's interesting! Tell me more about that.",
                    "I'm listening. Please continue.",
                    "That's a good point. What else would you like to share?",
                    "I understand. How can I help you further?",
                    "That's fascinating! Can you elaborate on that?",
                    "I'm processing that. What made you think of this?",
                    "That's worth discussing. What's your perspective on this?",
                    "I'm following along. What else comes to mind?",
                    "That's insightful! Tell me more about your thoughts.",
                    "I'm engaged in our conversation. What would you like to explore next?"
                ]
            
            # Use a more random selection instead of predictable cycling
            import random
            response = random.choice(responses)
        
        # Update conversation history
        conversation_history[session_id].extend([user_message, response])
        
        # Keep only last 20 exchanges to prevent memory issues
        if len(conversation_history[session_id]) > 40:
            conversation_history[session_id] = conversation_history[session_id][-40:]
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/status')
def status():
    """Check chatbot status"""
    return jsonify({
        'status': 'running',
        'chatbot_initialized': chatbot_instance is not None,
        'tokenizer_initialized': tokenizer_instance is not None,
        'intents_loaded': intents_data is not None,
        'intents_count': len(intents_data.get('intents', [])) if intents_data else 0,
        'conversation_sessions': len(conversation_history),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history for a session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_history:
            conversation_history[session_id] = []
        
        return jsonify({'status': 'cleared', 'session_id': session_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get available intents"""
    if intents_data:
        intent_tags = [intent['tag'] for intent in intents_data.get('intents', [])]
        return jsonify({'intents': intent_tags})
    return jsonify({'intents': []})

if __name__ == '__main__':
    # Initialize chatbot in a separate thread to avoid blocking
    init_thread = threading.Thread(target=initialize_chatbot_globals, daemon=True)
    init_thread.start()
    
    # Wait a moment for initialization
    time.sleep(2)
    
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting chatbot web server on port {port}")
    print(f"Open your browser and go to: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
