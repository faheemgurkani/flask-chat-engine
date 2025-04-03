# app/routes/api.py
from flask import Blueprint, request, jsonify
from app.services.chatbot import process_user_input

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/chat", methods=["POST"])
def get_bot_response():
    """API endpoint for chatbot responses"""
    user_input = request.form.get("msg")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    bot_response = process_user_input(user_input)
    
    return jsonify({"bot_response": bot_response})