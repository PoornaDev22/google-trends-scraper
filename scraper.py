import os
import json
import requests
import pandas as pd
from datetime import datetime

# Configuration
SCRAPER_API_KEY = '7225fc2f1a7477e19ab5fc93c751305b'
SCRAPER_API_URL = 'http://api.scraperapi.com'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'

class TrendFetcher:
    def __init__(self):
        self.session = requests.Session()

    def fetch_via_scraperapi(self, url):
        print(f"➡️  Fetching via ScraperAPI: {url}")
        params = {
            'api_key': SCRAPER_API_KEY,
            'url': url,
            'render': 'true',
            'country_code': 'us'
        }

        headers = {
            'User-Agent': USER_AGENT,
            'Referer': 'https://trends.google.com/trends/trendingsearches/daily?geo=US'
        }

        try:
            response = self.session.get(SCRAPER_API_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"❌ ScraperAPI error: {e}")
            return None

    def get_google_trends(self):
        print("📡 Fetching Google Trends JSON...")
        api_url = "https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-330&geo=US&ns=15"
        response = self.fetch_via_scraperapi(api_url)

        if not response or not response.text.startswith(")]}',"):
            print("❌ Failed to fetch or parse Google Trends JSON.")
            return []

        json_str = response.text[5:]  # Strip anti-JSON prefix
        try:
            data = json.loads(json_str)
            trends_raw = data.get("default", {}).get("trendingSearchesDays", [])[0].get("trendingSearches", [])
            keywords = [t["title"]["query"] for t in trends_raw if "title" in t and "query" in t["title"]]
            print(f"✅ Extracted {len(keywords)} keywords")
            return keywords[:10]
        except Exception as e:
            print(f"❌ JSON parsing error: {e}")
            return []

    def save_to_csv(self, keywords):
        if not keywords:
            print("⚠️ No keywords found. Skipping save.")
            return

        df = pd.DataFrame(keywords, columns=["Keyword"])
        os.makedirs("data", exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"data/trending_{today}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(keywords)} keywords to {filename}")

if __name__ == "__main__":
    fetcher = TrendFetcher()
    keywords = fetcher.get_google_trends()
    fetcher.save_to_csv(keywords)
