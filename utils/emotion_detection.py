from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_emotion(text):
    """Detect emotion in text using OpenAI's GPT model."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Detect the emotional tone of this text."},
            {"role": "user", "content": text}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()