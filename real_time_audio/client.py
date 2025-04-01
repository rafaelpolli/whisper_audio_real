import sounddevice as sd
import numpy as np
import base64
import websocket
import threading

API_URL = "ws://localhost:5001/ws"  # Transcription API WebSocket URL
SAMPLE_RATE = 16000  # Whisper's expected sample rate
CHUNK_SIZE = 1024  # Number of samples per chunk

def on_message(ws, message):
    print("Transcription:", message)

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed:", close_msg)

def on_open(ws):
    print("Connected to Transcription API. Recording...")
    
    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_data = indata.astype(np.int16).tobytes()
        encoded_audio = base64.b64encode(audio_data).decode('utf-8')
        ws.send(encoded_audio)
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=CHUNK_SIZE):
        input("Press Enter to stop recording...\n")
    
    ws.close()

def start_recording():
    ws = websocket.WebSocketApp(API_URL, 
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()
    ws_thread.join()
    print("Disconnected.")

if __name__ == "__main__":
    start_recording()
