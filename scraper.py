# scraper.py
from playwright.sync_api import sync_playwright
import re, json, os
from datetime import datetime

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://nekto.me/audiochat")
    page.wait_for_timeout(4000)
    match = re.search(r'(\d+)\s*пользователей', page.content())
    users = int(match.group(1)) if match else 0
    browser.close()

data = []
if os.path.exists('data.json'):
    with open('data.json') as f:
        data = json.load(f)
data.append({'time': datetime.now().isoformat(), 'users': users})
with open('data.json', 'w') as f:
    json.dump(data[-5000:], f)
