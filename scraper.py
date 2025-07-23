from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os

# Setup headless Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start driver
driver = webdriver.Chrome(options=options)

# Go to Google Trends
url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
driver.get(url)
time.sleep(5)  # wait for JS to render

# Parse HTML
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Extract titles
titles = [tag.text for tag in soup.select("div.feed-item div.details-top a")]
if not titles:
    print("No trending titles found.")
else:
    print(f"Found {len(titles)} trending topics.")

# Save to CSV
today = datetime.now().strftime("%Y-%m-%d")
os.makedirs("output", exist_ok=True)
df = pd.DataFrame(titles, columns=["Trending Searches"])
df.to_csv(f"output/trending_{today}.csv", index=False)
print(f"Saved to output/trending_{today}.csv")
