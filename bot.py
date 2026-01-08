def main():
    data = fetch_api()

    # API вернул список элементов
    if isinstance(data, list):
        if not data:
            return  # пусто

        # чаще всего "новое" — либо первый, либо последний
        item = data[0]   # если у тебя новые сверху
        # item = data[-1]  # если у тебя новые снизу

    # API вернул объект
    elif isinstance(data, dict):
        item = data.get("data", data)
    else:
        return

    current_id = str(item.get("id", item.get("uid", item.get("timestamp", ""))))
    if not current_id:
        # если нет id, используем сам текст как маркер
        current_id = str(item)

    last_id = get_last_id()
    if current_id == last_id:
        return

    text = item.get("text") or item.get("message") or item.get("title") or str(item)
    send(text)
    save_last_id(current_id)
