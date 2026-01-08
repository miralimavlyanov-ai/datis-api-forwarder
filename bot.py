import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_URL = os.environ["API_URL"]

STATE_FILE = "last_id.txt"

def get_last_id():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_id(value):
    with open(STATE_FILE, "w") as f:
        f.write(str(value))

def fetch_api():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    return r.json()

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    }, timeout=10)

def main():
    data = fetch_api()

    item = data["data"]
    current_id = str(item["id"])

    if current_id == get_last_id():
        return

    send(item["text"])
    save_last_id(current_id)

main()
