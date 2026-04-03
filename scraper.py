# scraper.py
from playwright.sync_api import sync_playwright, TimeoutError
import re, json, os
from datetime import datetime, timezone

def get_users():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://nekto.me/audiochat", timeout=60000)
            page.wait_for_timeout(3000)  # небольшая пауза, чтобы загрузилась статистика

            # Если есть конкретный селектор для числа пользователей, лучше заменить "body" на него
            text = page.inner_text("body")
            match = re.search(r'\b\d{3,6}\b', text)
            if match:
                return int(match.group())
    except TimeoutError:
        print("Ошибка: страница не загрузилась за 60 секунд")
    except Exception as e:
        print("Ошибка при получении данных:", e)
    finally:
        try:
            browser.close()
        except:
            pass
    return 0

def save_data(users):
    data_file = "data.json"
    data = []
    if os.path.exists(data_file):
        try:
            with open(data_file) as f:
                data = json.load(f)
        except Exception:
            data = []

    data.append({
        "time": datetime.now(timezone.utc).isoformat(),
        "users": users
    })

    with open(data_file, "w") as f:
        json.dump(data[-5000:], f, indent=2)

if __name__ == "__main__":
    users = get_users()
    print(f"Пользователей: {users}")
    save_data(users)
