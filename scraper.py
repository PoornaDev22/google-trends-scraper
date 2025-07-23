# scraper.py

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

API_KEY = "7225fc2f1a7477e19ab5fc93c751305b"
SCRAPER_API_URL = "http://api.scraperapi.com"

TARGET_URL = "https://trends.google.com/trending?geo=US"

def fetch_trending_keywords():
    params = {
        'api_key': API_KEY,
        'url': TARGET_URL,
        'render': 'true'
    }
    response = requests.get(SCRAPER_API_URL, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    for item in soup.select("div.feed-item .title"):
        title_text = item.get_text(strip=True)
        if title_text:
            titles.append(title_text)

    return titles

def save_keywords(keywords):
    date_str = datetime.now().strftime('%Y-%m-%d')
    with open(f"trending_{date_str}.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Keyword"])
        for keyword in keywords:
            writer.writerow([keyword])
    print(f"Saved {len(keywords)} keywords.")

if __name__ == "__main__":
    keywords = fetch_trending_keywords()
    if keywords:
        save_keywords(keywords)
    else:
        print("No keywords found.")
