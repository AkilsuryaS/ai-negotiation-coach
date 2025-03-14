import pyaudio
import numpy as np
import soundfile as sf
import os
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Audio parameters
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate (16 kHz)
CHUNK = 1024  # Frames per buffer
SILENCE_THRESHOLD = 500  # Silence threshold (adjust as needed)
SILENCE_TIMEOUT = 2  # Silence timeout in seconds

def record_audio():
    """
    Record audio until speech ends, using energy-based silence detection.
    """
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording... Speak now.")

    frames = []
    silence_frames = 0
    recording = False

    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Ensure the audio data is valid
        if len(audio_data) == 0:
            continue  # Skip empty chunks

        # Calculate the energy (volume) of the audio chunk
        energy = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))

        # Check if the energy exceeds the silence threshold
        if energy > SILENCE_THRESHOLD:
            recording = True
            silence_frames = 0
        else:
            silence_frames += 1

        # Stop recording if silence exceeds the timeout
        if recording and silence_frames > SILENCE_TIMEOUT * (RATE / CHUNK):
            print("Speech ended. Stopping recording.")
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Combine recorded frames into a single array
    audio = np.frombuffer(b''.join(frames), dtype=np.int16)
    return audio

def transcribe_audio(audio, samplerate=16000):
    """
    Transcribe audio using OpenAI's Whisper API.
    """
    # Save the recorded audio to a temporary file
    sf.write("temp.wav", audio, samplerate)
    
    # Transcribe the audio file using OpenAI's Whisper API
    with open("temp.wav", "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

def text_to_speech(text, filename="response.mp3"):
    """
    Convert text to speech and play it.
    """
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    os.system(f"afplay {filename}")  # For macOS. Use "start" for Windows or "mpg321" for Linux.