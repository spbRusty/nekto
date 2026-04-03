# scraper.py
from playwright.sync_api import sync_playwright
import re, json, os
from datetime import datetime

users = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://nekto.me/audiochat", timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")

    match = re.search(r'\d{3,6}', text)
    if match:
        users = int(match.group())

    browser.close()

data = []

if os.path.exists("data.json"):
    with open("data.json") as f:
        data = json.load(f)

data.append({
    "time": datetime.utcnow().isoformat(),
    "users": users
})

with open("data.json", "w") as f:
    json.dump(data[-5000:], f)
