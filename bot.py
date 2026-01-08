import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    print("TG status:", r.status_code)
    print("TG response:", r.text[:1000])
    r.raise_for_status()

if __name__ == "__main__":
    send("TEST_FROM_GITHUB_ACTIONS ✅")
