import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using Gemini 1.5 Flash as it is the recommended default for text tasks
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found in .env file. Chatbot will be disabled.")

def get_chatbot_response(message, context=""):
    """
    Sends a message to the Gemini API and returns the response.
    Includes context about the application.
    """
    if not model:
        return "I'm sorry, my AI capabilities are currently disabled because the API key is missing."

    system_prompt = (
        "You are a helpful AI assistant for a Community Needs Aggregator and Volunteer Matching System. "
        "Your role is to help NGOs and Volunteers navigate the platform, understand how to report issues, "
        "and explain how the matching system works. "
        "Keep your answers concise, friendly, and helpful. "
    )
    
    if context:
        system_prompt += f"\nHere is some context about the current state of the application:\n{context}\n"

    try:
        response = model.generate_content(f"{system_prompt}\nUser: {message}")
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I encountered an error while processing your request. Please try again later."
