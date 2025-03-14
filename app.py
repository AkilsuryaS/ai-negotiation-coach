import streamlit as st
import streamlit.components.v1 as components
import openai
import os
import json
import io
import base64
from datetime import datetime
from dotenv import load_dotenv
from utils.voice_processing import record_audio, transcribe_audio, text_to_speech
from utils.emotion_detection import detect_emotion
from utils.feedback_metrics import generate_feedback
from utils.negotiation_logic import get_ai_response
from streamlit_lottie import st_lottie
import requests
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to load a Lottie animation from a URL
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_mic = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_pojzngga.json")

# App title and description
st.title("AI Negotiation Coach")
st.write("Practice your negotiation skills with AI in real-time!")

# Initialize session state for conversation history, negotiation status,
# loaded session (from previous negotiations), and current session.
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "negotiation_started" not in st.session_state:
    st.session_state.negotiation_started = False
if "loaded_session" not in st.session_state:
    st.session_state.loaded_session = None
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# Sidebar: Settings and Previous Negotiations
with st.sidebar:
    st.header("Settings")
    negotiation_scenario = st.text_input("Enter the negotiation scenario:")
    conversation_style = st.selectbox("Select conversation style:", ["Collaborative", "Aggressive", "Neutral"])
    st.write("Click 'Start Negotiation' to begin.")

    # Load previous negotiation sessions (if any)
    previous_sessions = []
    if os.path.exists("negotiation_sessions.json"):
        with open("negotiation_sessions.json", "r") as f:
            for line in f:
                try:
                    session = json.loads(line)
                    previous_sessions.append(session)
                except json.JSONDecodeError:
                    continue

    if previous_sessions:
        st.header("Previous Negotiations")
        # Create a list of session identifiers (timestamp and scenario)
        session_options = ["-- None --"] + [f"{session['timestamp']} - {session['scenario']}" for session in previous_sessions]
        selected_session = st.selectbox("Select a previous negotiation session:", session_options)
        if selected_session != "-- None --":
            selected_index = session_options.index(selected_session) - 1  # adjust for placeholder
            st.session_state.loaded_session = previous_sessions[selected_index]
        else:
            st.session_state.loaded_session = None
    else:
        st.write("No previous negotiations found.")

# Function to handle a negotiation round (recording, transcribing, and AI response)
def negotiation_round():
    st.write("Speak into your microphone.")
    st_lottie(lottie_mic, speed=1, height=200, key=f"mic_animation_{len(st.session_state.conversation_history)}")
    st.write("Recording...")
    audio = record_audio()
    st.write("Recording complete. Transcribing...")
    user_input = transcribe_audio(audio)
    st.write(f"**You said:** {user_input}")
    # Detect emotion in the user's input
    emotion = detect_emotion(user_input)
    st.write(f"**Detected emotion:** {emotion}")
    # Get AI response based on scenario, style, emotion, and user input
    ai_response = get_ai_response(negotiation_scenario, conversation_style, emotion, user_input)
    # Convert the AI response to speech
    text_to_speech(ai_response)
    # Append this turn to the conversation history
    st.session_state.conversation_history.append({"user": user_input, "ai": ai_response})

# --- Negotiation Controls ---
if not st.session_state.negotiation_started:
    if st.button("Start Negotiation"):
        st.session_state.negotiation_started = True
        negotiation_round()

if st.session_state.negotiation_started:
    col1, col2 = st.columns(2)
    if col1.button("Continue Negotiating"):
        negotiation_round()
    if col2.button("End Negotiation"):
        st.write("Negotiation ended. Here's your final feedback:")
        # Generate feedback for the session
        feedback = generate_feedback(st.session_state.conversation_history, negotiation_scenario)
        st.write("### Feedback Metrics")
        col_feedback1, col_feedback2, col_feedback3 = st.columns(3)
        with col_feedback1:
            st.metric("Clarity Score", f"{feedback['score']['Clarity']:.2f}/10")
            st.progress(feedback['score']['Clarity'] / 10)
        with col_feedback2:
            st.metric("Persuasiveness Score", f"{feedback['score']['Persuasiveness']:.2f}/10")
            st.progress(feedback['score']['Persuasiveness'] / 10)
        with col_feedback3:
            st.metric("Total Score", f"{feedback['score']['Total']:.2f}/10")
            st.progress(feedback['score']['Total'] / 10)
        st.write("### Detailed Feedback")
        st.markdown(feedback['points_to_consider'])
        st.markdown(feedback['performance_analysis'])
        st.write("#### Areas for Improvement")
        for improvement in feedback['improvements']:
            st.write(f"- {improvement}")
        # Save the current session data (includes conversation and feedback)
        st.session_state.current_session = {
            "scenario": negotiation_scenario,
            "style": conversation_style,
            "conversation": st.session_state.conversation_history,
            "feedback": feedback,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Also, append the session to the JSON file
        with open("negotiation_sessions.json", "a") as f:
            f.write(json.dumps(st.session_state.current_session) + "\n")
        # End the negotiation session (but keep the conversation visible)
        st.session_state.negotiation_started = False

# --- Main Chat Container ---
st.subheader("Negotiation Chat")
# If a previous session is loaded, display that; otherwise, show the current conversation.
if st.session_state.loaded_session is not None:
    st.info("**Showing Previous Negotiation Chat**")
    chat_to_display = st.session_state.loaded_session["conversation"]
else:
    chat_to_display = st.session_state.conversation_history

for entry in chat_to_display:
    with st.chat_message("user"):
        st.markdown(entry["user"])
    with st.chat_message("assistant"):
        st.markdown(entry["ai"])

# --- Export as PDF ---
st.subheader("Export Session as PDF")
# Determine which session to export:
if st.session_state.loaded_session is not None:
    session_data = st.session_state.loaded_session
elif st.session_state.current_session is not None:
    session_data = st.session_state.current_session
else:
    session_data = None

if session_data:
    if st.button("Export as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Negotiation Session", ln=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Scenario: {session_data['scenario']}", ln=1)
        pdf.cell(0, 10, f"Style: {session_data['style']}", ln=1)
        pdf.cell(0, 10, f"Timestamp: {session_data['timestamp']}", ln=1)
        pdf.ln(10)
        pdf.cell(0, 10, "Conversation:", ln=1)
        for i, entry in enumerate(session_data['conversation']):
            pdf.multi_cell(0, 10, f"Turn {i+1}:\nYou: {entry['user']}\nAI: {entry['ai']}\n")
            pdf.ln(5)
        pdf.ln(10)
        pdf.cell(0, 10, "Feedback:", ln=1)
        pdf.multi_cell(0, 10, f"Clarity Score: {session_data['feedback']['score']['Clarity']:.2f}/10")
        pdf.multi_cell(0, 10, f"Persuasiveness Score: {session_data['feedback']['score']['Persuasiveness']:.2f}/10")
        pdf.multi_cell(0, 10, f"Total Score: {session_data['feedback']['score']['Total']:.2f}/10")
        pdf.ln(5)
        pdf.multi_cell(0, 10, "Performance Summary:")
        pdf.multi_cell(0, 10, session_data['feedback']['summary'])
        pdf.ln(5)
        pdf.cell(0, 10, "Areas for Improvement:", ln=1)
        for improvement in session_data['feedback']['improvements']:
            pdf.multi_cell(0, 10, f"- {improvement}")
        # Generate PDF data as bytes (replace problematic characters)
        pdf_data = pdf.output(dest='S').encode('latin1', errors='replace')
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        # Create an HTML snippet with a hidden download link that auto-clicks
        html = f'''
        <html>
          <body>
            <a id="downloadLink" style="display: none;" href="data:application/pdf;base64,{pdf_base64}" download="negotiation_session.pdf">Download PDF</a>
            <script type="text/javascript">
              document.getElementById("downloadLink").click();
            </script>
          </body>
        </html>
        '''
        components.html(html, height=0, scrolling=False)
else:
    st.info("No session available to export as PDF.")
