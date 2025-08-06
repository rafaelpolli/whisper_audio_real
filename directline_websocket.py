import json
import requests
import websocket
import threading

# Replace with your Direct Line secret
DIRECT_LINE_SECRET = "YOUR_DIRECT_LINE_SECRET"
DIRECT_LINE_URL = "https://directline.botframework.com/v3/directline/conversations"

# Step 1: Start a conversation
headers = {
    "Authorization": f"Bearer {DIRECT_LINE_SECRET}"
}
response = requests.post(DIRECT_LINE_URL, headers=headers)
response_data = response.json()

conversation_id = response_data["conversationId"]
stream_url = response_data["streamUrl"]

print(f"Conversation started. ID: {conversation_id}")
print(f"Stream URL: {stream_url}")


# Step 2: Define WebSocket event handlers
def on_message(ws, message):
    data = json.loads(message)
    print("\n🔹 Message received:")
    print(json.dumps(data, indent=2))


def on_error(ws, error):
    print("\n❌ Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("\n🔒 WebSocket closed")


def on_open(ws):
    print("\n✅ WebSocket connection opened")


# Step 3: Connect to WebSocket
ws_app = websocket.WebSocketApp(
    stream_url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws_app.on_open = on_open

# Run WebSocket in a separate thread
thread = threading.Thread(target=ws_app.run_forever)
thread.daemon = True
thread.start()


# Step 4: Send a message to the bot (via REST API)
send_message_url = f"{DIRECT_LINE_URL}/{conversation_id}/activities"

message_payload = {
    "type": "message",
    "from": {"id": "user1"},
    "text": "Hello from Python via Direct Line WebSocket!"
}

send_response = requests.post(send_message_url, headers=headers, json=message_payload)

print("\n📤 Message sent to bot")
print("Response:", send_response.status_code, send_response.text)


# Keep the script running to listen for responses
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nExiting...")
    ws_app.close()
