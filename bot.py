import os
import requests
import json

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_URL = os.environ["API_URL"]

def fetch_api():
    r = requests.get(API_URL, timeout=20)
    print("API status:", r.status_code)
    print("API response (first 1000 chars):", r.text[:1000])
    r.raise_for_status()
    return r.json()

def send_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    r = requests.post(url, json=payload, timeout=20)
    print("TG status:", r.status_code)
    print("TG response:", r.text[:1000])

    r.raise_for_status()

def pick_item(data):
    # Если пришёл список — берём первый элемент
    if isinstance(data, list):
        if not data:
            return None
        return data[0]

    # Если пришёл dict — попробуем угадать где полезное
    if isinstance(data, dict):
        # часто бывает {"data":[...]} или {"results":[...]}
        for key in ("data", "results", "items"):
            if key in data:
                val = data[key]
                if isinstance(val, list) and val:
                    return val[0]
                if isinstance(val, dict):
                    return val
        return data

    return None

def main():
    data = fetch_api()
    item = pick_item(data)

    if item is None:
        print("No item found in API response.")
        return

    print("Picked item type:", type(item))
    print("Picked item (json):", json.dumps(item, ensure_ascii=False)[:1000])

    # Пытаемся достать текст разными ключами
    if isinstance(item, dict):
        text = item.get("text") or item.get("message") or item.get("title") or item.get("description")
    else:
        text = str(item)

    if not text:
        print("No text field found in item.")
        return

    print("Text to send (first 500 chars):", text[:500])
    send_to_telegram(text)

if __name__ == "__main__":
    main()
