from playwright.sync_api import sync_playwright
import re, json, os
from datetime import datetime, timezone

# Получение количества пользователей
users = 0
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://nekto.me/audiochat", timeout=60000)
    page.wait_for_timeout(3000)  # 3 секунды достаточно
    text = page.inner_text("body")
    match = re.search(r'\d{3,6}', text)
    if match:
        users = int(match.group())
    browser.close()

# Загрузка старых данных
data = []
if os.path.exists("data.json"):
    try:
        with open("data.json") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []

# Добавление новой записи
data.append({
    "time": datetime.now(timezone.utc).isoformat(),  # timezone-aware UTC
    "users": users
})

# Ограничение истории до последних 5000 записей
with open("data.json", "w") as f:
    json.dump(data[-5000:], f, ensure_ascii=False)
