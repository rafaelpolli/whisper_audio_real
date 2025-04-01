import sounddevice as sd
import numpy as np
import base64
import socketio

# WebSocket client setup
sio = socketio.Client()
API_URL = "http://localhost:5001"  # Transcription API URL

# Audio settings
SAMPLE_RATE = 16000  # Whisper's expected sample rate
CHUNK_SIZE = 1024  # Number of samples per chunk

@sio.on('transcription')
def on_transcription(data):
    print("Transcription:", data['text'])

def callback(indata, frames, time, status):
    """ Callback function to send audio in real-time """
    if status:
        print(status)
    audio_data = indata.astype(np.int16).tobytes()
    encoded_audio = base64.b64encode(audio_data).decode('utf-8')
    sio.emit('audio_chunk', encoded_audio)

def start_recording():
    sio.connect(API_URL)
    print("Connected to Transcription API. Recording...")
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=CHUNK_SIZE):
        input("Press Enter to stop recording...\n")
    
    sio.disconnect()
    print("Disconnected.")

if __name__ == "__main__":
    start_recording()