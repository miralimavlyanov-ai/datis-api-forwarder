import os
import json
import requests
import hashlib

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_URL = os.environ["API_URL"]

STATE_FILE = "last_hash.txt"

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_state(value: str):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(value)

def fetch_api():
    r = requests.get(API_URL, timeout=20)
    print("API status:", r.status_code)
    r.raise_for_status()
    return r.json()

def send(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    print("TG status:", r.status_code)
    print("TG response:", r.text[:500])
    r.raise_for_status()

def pick_item(data):
    # Если API вернул список — берём "самое новое"
    if isinstance(data, list):
        if not data:
            return None
        # Попробуем угадать: если есть id и он растёт, берём max(id)
        if all(isinstance(x, dict) and ("id" in x) for x in data):
            return max(data, key=lambda x: x.get("id", 0))
        return data[0]  # иначе просто первый

    # Если API вернул dict — попробуем найти внутри список/объект
    if isinstance(data, dict):
        for key in ("data", "results", "items"):
            if key in data:
                v = data[key]
                if isinstance(v, list) and v:
                    return v[0]
                if isinstance(v, dict):
                    return v
        return data

    return None

def extract_text(item):
    # Подстройка под разные API: перечисли возможные поля
    for k in ("text", "message", "content", "body", "description", "title"):
        if isinstance(item, dict) and item.get(k):
            return str(item[k])
    return None

def main():
    data = fetch_api()
    item = pick_item(data)

    if item is None:
        print("No item found.")
        return

    text = extract_text(item)
    if not text:
        print("No text field found in item. Item keys:", list(item.keys()) if isinstance(item, dict) else type(item))
        print("Item preview:", json.dumps(item, ensure_ascii=False)[:800])
        return

    # Антидубликат: хэш текста
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if h == load_state():
        print("No changes (same hash).")
        return

    send(text)
    save_state(h)

if __name__ == "__main__":
    main()
