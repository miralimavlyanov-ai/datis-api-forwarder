import os
import time
import requests
import hashlib
from datetime import datetime, timezone

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_URL = os.environ["API_URL"]

STATE_FILE = "last_hash.txt"

def load_hash() -> str:
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_hash(h: str) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(h)

def send(text: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    ).raise_for_status()

def fetch_json_no_cache():
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    # уникальный параметр, чтобы пробивать CDN-кэш
    url = f"{API_URL}?_ts={int(time.time())}"
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    data = fetch_json_no_cache()

    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return

    item = data[0]
    datis = (item.get("datis") or "").strip()
    if not datis:
        return

    h = hashlib.sha256(datis.encode("utf-8")).hexdigest()
    if h == load_hash():
        return

    polled_utc = datetime.now(timezone.utc).strftime("%H:%MZ %d-%b-%Y")
    updated_at = (item.get("updatedAt") or "").strip()

    # Сообщение как ты хочешь + одна техстрока (для понимания задержек)
    msg = datis + f"\n\nPolled (UTC): {polled_utc}"
    if updated_at:
        msg += f"\nAPI updatedAt: {updated_at}"

    send(msg)
    save_hash(h)

if __name__ == "__main__":
    main() 