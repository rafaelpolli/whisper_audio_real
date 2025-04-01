import wave
import base64
from flask import Flask
from flask_socketio import SocketIO, emit
from transformers import pipeline

# Load Whisper model from transformers
whisper_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Flask WebSocket API
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('audio_chunk')
def handle_audio(data):
    audio_bytes = base64.b64decode(data)

    # Save audio chunk as a temporary WAV file
    with wave.open("temp_audio.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_bytes)
    
    # Transcribe using Whisper with Transformers
    result = whisper_pipe("temp_audio.wav")
    text = result["text"]
    
    emit('transcription', {'text': text})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)