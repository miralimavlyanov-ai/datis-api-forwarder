import os
import requests
import hashlib

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

def main():
    # Получаем JSON
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()
    data = r.json()

    # Твой формат: список с 1 объектом
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return

    datis = (data[0].get("datis") or "").strip()
    if not datis:
        return

    # Фильтрация/антидубликат строго по datis
    h = hashlib.sha256(datis.encode("utf-8")).hexdigest()
    if h == load_hash():
        return

    # Отправляем строго datis (как ты хочешь)
    send(datis)

    # Запоминаем хэш datis
    save_hash(h)

if __name__ == "__main__":
    main()
