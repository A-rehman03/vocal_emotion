from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys

# Import chatbot functions
from chatbot3 import enhanced_match_intent, generate_response, initialize_chatbot, load_intents

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables for chatbot
chatbot = None
tokenizer = None
intents = None

def initialize_chatbot_globals():
    """Initialize chatbot components globally"""
    global chatbot, tokenizer, intents
    
    if chatbot is None or tokenizer is None:
        chatbot, tokenizer = initialize_chatbot()
    
    if intents is None:
        intents = load_intents()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from React frontend"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize chatbot if not already done
        initialize_chatbot_globals()
        
        # Try to match intent first
        response = enhanced_match_intent(message, intents)
        
        if not response:
            # Use transformer model for response
            response = generate_response(chatbot, tokenizer, message, [])
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/learn', methods=['POST'])
def learn_intent():
    """Learn new intent from user feedback"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        response = data.get('response', '')
        
        if not text or not response:
            return jsonify({'error': 'Text and response required'}), 400
        
        # Update intents
        from chatbot3 import update_intents
        result = update_intents(text, response)
        
        if result:
            # Reload intents
            global intents
            intents = load_intents()
            
            return jsonify({
                'message': 'Intent learned successfully',
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'Failed to learn intent',
                'status': 'error'
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'JTalk API is running'
    })

if __name__ == '__main__':
    print("Starting JTalk API server...")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
