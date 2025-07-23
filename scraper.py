# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os

# Setup headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Launch Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Load Google Trends daily trending page
url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
driver.get(url)
time.sleep(5)  # Wait for JS to load

# Parse the page
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extract trending search titles
titles = [e.text for e in soup.select("div.feed-item div.details-top a")]
if not titles:
    print("No trending titles found!")
else:
    print("Found trending titles:", titles)

# Save to CSV
today = datetime.now().strftime("%Y-%m-%d")
df = pd.DataFrame(titles, columns=["Trending Searches"])
os.makedirs("output", exist_ok=True)
df.to_csv(f"output/trending_{today}.csv", index=False)
print(f"Saved to output/trending_{today}.csv")
