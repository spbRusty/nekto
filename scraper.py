from playwright.sync_api import sync_playwright
import re, json, os
from datetime import datetime, timezone

users = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # wait_until="networkidle" ждет, пока страница полностью не прогрузится
    page.goto("https://nekto.me/audiochat", wait_until="networkidle", timeout=60000)
    
    # Небольшая пауза, чтобы JS на сайте точно успел отрендерить цифры
    page.wait_for_timeout(5000) 
    
    text = page.inner_text("body")
    match = re.search(r'\d{3,6}', text)
    if match:
        users = int(match.group())
        print(f"Найдено пользователей онлайн: {users}")
    else:
        print("Не удалось найти количество пользователей.")
        
    browser.close()

data = []

# Читаем старые данные
if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

# Добавляем новые (используем правильный timezone)
if users > 0:
    data.append({
        "time": datetime.now(timezone.utc).isoformat(),
        "users": users
    })

# Сохраняем последние 5000 записей
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data[-5000:], f)
