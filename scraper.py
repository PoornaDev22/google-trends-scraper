# scraper.py

import json
import time
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import csv

SCRAPER_API_KEY = '7225fc2f1a7477e19ab5fc93c751305b'
SCRAPER_API_URL = 'http://api.scraperapi.com'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

class TrendFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})

    def fetch_via_scraperapi(self, url, params=None):
        params = params or {}
        params.update({
            'api_key': SCRAPER_API_KEY,
            'url': url,
            'render': 'true'
        })

        for attempt in range(3):
            try:
                response = self.session.get(SCRAPER_API_URL, params=params, timeout=30)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    time.sleep((attempt + 1) * 10)
                else:
                    print(f"HTTP {response.status_code}")
            except Exception as e:
                print(f"Request error: {e}")
                time.sleep((attempt + 1) * 5)
        return None

    def get_google_trends(self):
    print("Fetching Google Trends JSON...")

    api_url = "https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-330&geo=US&ns=15"
    response = self.fetch_via_scraperapi(api_url)

    if not response or not response.text.startswith(")]}',"):
        print("❌ Failed to fetch or parse Google Trends JSON.")
        return []

    # Remove anti-JSON hijacking prefix
    json_str = response.text[5:]
    try:
        data = json.loads(json_str)
        trends_raw = data.get("default", {}).get("trendingSearchesDays", [])[0].get("trendingSearches", [])
        keywords = [t["title"]["query"] for t in trends_raw if "title" in t and "query" in t["title"]]
        print(f"✅ Extracted {len(keywords)} keywords from JSON")
        return keywords[:10]
    except Exception as e:
        print(f"❌ JSON parsing error: {e}")
        return []

    def _parse_google_v1(self, html):
        soup = BeautifulSoup(html, 'lxml')
        items = soup.select('div.details-top a.title, a.title-text, div.title > a')
        return [{"keyword": item.get_text().strip()} for item in items[:10] if item.get_text().strip()]

    def _parse_google_v2(self, html):
        pattern = re.compile(r'"title":"([^"]{4,}?)"')
        matches = pattern.findall(html)
        return [{"keyword": match.strip()} for match in matches[:10]]

    def _parse_google_fallback(self, html):
        soup = BeautifulSoup(html, 'lxml')
        found = []
        for item in soup.find_all(['a', 'div', 'span']):
            text = item.get_text().strip()
            if (20 <= len(text) <= 100) and ' ' in text:
                found.append({"keyword": text})
            if len(found) >= 10:
                break
        return found

    def save_to_csv(self, keywords):
        os.makedirs("data", exist_ok=True)
        date_str = datetime.now().strftime('%Y-%m-%d')
        path = f"data/trending_{date_str}.csv"
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Keyword"])
            for kw in keywords:
                writer.writerow([kw])
        print(f"✅ Saved to {path}")
        return path

def main():
    fetcher = TrendFetcher()
    keywords = fetcher.get_google_trends()
    if keywords:
        fetcher.save_to_csv(keywords)
    else:
        print("❌ No keywords found.")

if __name__ == "__main__":
    main()
