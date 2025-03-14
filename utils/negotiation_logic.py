from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(scenario, style, emotion, user_input):
    """
    Generate AI response based on negotiation scenario, style, emotion, and user input.
    """
    # Create a prompt that includes the scenario, style, emotion, and user input
    prompt = f"""
    You are role-playing as the person the user is negotiating with in the following scenario:
    Scenario: {scenario}
    Conversation Style: {style}
    User's Emotional Tone: {emotion}
    User's Input: "{user_input}"
    Respond as the counterpart in the scenario, keeping the conversation realistic and engaging.
    """
    
    # Generate the AI's response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()