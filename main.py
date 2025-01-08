from flask import Flask, request, jsonify
import os
import requests
import logging

app = Flask(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Basic logging setup
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST"])
def handle_webhook():
    try:
        # Parse the JSON body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty payload"}), 400

        # Log the received data for debugging
        print("Received data:", data)

        # Respond to Telegram or the client
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

def handle_update(update):
    """Processes the Telegram update."""
    chat_id = update.get("message", {}).get("chat", {}).get("id")
    text = update.get("message", {}).get("text", "")

    if text == "/start":
        send_message(chat_id, "Welcome to the bot!")
    else:
        send_message(chat_id, f"You said: {text}")


def send_message(chat_id, text):
    """Sends a message via the Telegram Bot API."""
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        logging.error(f"Failed to send message: {response.text}")
    else:
        logging.info(f"Message sent to chat_id {chat_id}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
