# AI Negotiation Coach

## Overview
The **AI Negotiation Coach** is a Streamlit-based web application designed to help users practice and improve their negotiation skills in real-time. The app uses OpenAI's GPT-4 for generating realistic negotiation responses, emotion detection to analyze the user's tone, and feedback metrics to provide actionable insights. Additionally, it supports voice input and output, making the interaction more natural and engaging.

## Features
- **Real-Time Negotiation Practice**: Engage in realistic negotiation scenarios with an AI counterpart.
- **Emotion Detection**: Analyze the emotional tone of your input to tailor the AI's response.
- **Voice Input/Output**: Speak into your microphone and receive spoken responses from the AI.
- **Feedback Metrics**: Receive detailed feedback on your negotiation performance, including clarity, persuasiveness, and areas for improvement.
- **Session History**: Save and review previous negotiation sessions.
- **Export as PDF**: Export your negotiation session and feedback as a PDF for offline review.

## Installation

### Prerequisites
- Python 3.8 or higher
- An OpenAI API key (you can get one from [OpenAI](https://platform.openai.com/))

## Project Structure:
```bash
AI-NEGOTIATION-COACH/
│
├── assets/                        # (Optional) Holds images, animations, or other assets
├── utils/
│   ├── emotion_detection.py       # Detects user’s emotional tone
│   ├── feedback_metrics.py        # Generates performance feedback and scores
│   ├── negotiation_logic.py       # Constructs prompts and fetches AI negotiation responses
│   └── voice_processing.py        # Records audio, transcribes it, and plays AI responses
│
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── README.md                      # Project README (this file)
├── .env                           # Environment variables (not committed to version control)
└── negotiation_sessions.json      # (Generated) Logs past negotiation sessions
```

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-negotiation-coach.git
   cd ai-negotiation-coach ```

2. **Set Up Environment Variables**:
- Create a .env file in the root directory.
- Add your OpenAI API key to the .env file
```bash
OPENAI_API_KEY=your-api-key-here
```
3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the Application:**
```bash
streamlit run app.py
```
5. **Access the App**:
- Open your web browser and navigate to `http://localhost:8501`.

## Usage
**Starting a Negotiation**
1. **Enter the Negotiation Scenario:** Provide a brief description of the negotiation scenario (e.g., "Salary negotiation with your manager").
2. **Select Conversation Style:** Choose from "Collaborative", "Aggressive", or "Neutral" to define the AI's response style.
3. **Click "Start Negotiation":** Begin the negotiation by speaking into your microphone.

**During the Negotiation**
- **Speak Clearly:** The app will record your voice and transcribe it into text.
- **AI Response:** The AI will respond based on the scenario, style, and detected emotion in your input.
- **Continue or End:** You can continue the negotiation or end it to receive feedback.

**Feedback and Analysis:**
- **Clarity and Persuasiveness Scores:** Receive scores based on how clearly and persuasively you communicated.
- **Areas for Improvement:** Get actionable tips to improve your negotiation skills.
- **Export as PDF:** Save your session and feedback as a PDF for future reference.


