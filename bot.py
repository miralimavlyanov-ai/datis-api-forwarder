import os
import requests
import hashlib

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_URL = os.environ["API_URL"]

STATE_FILE = "last_hash.txt"

def load_hash():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_hash(h):
    with open(STATE_FILE, "w") as f:
        f.write(h)

def main():
    text = requests.get(API_URL, timeout=20).text.strip()
    current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    if current_hash == load_hash():
        return  # текст не изменился — молчим

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )

    save_hash(current_hash)

if __name__ == "__main__":
    main()
