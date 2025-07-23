from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import os
import time

# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)

# Open the Google Trends page
url = "https://trends.google.com/trending?geo=US"
driver.get(url)
time.sleep(5)  # Wait for dynamic content to load

# Extract trending keywords
elements = driver.find_elements(By.CSS_SELECTOR, "div.feed-item span.title-text")
keywords = [el.text.strip() for el in elements if el.text.strip()]

driver.quit()

# Save results
if keywords:
    os.makedirs("data", exist_ok=True)
    filename = f"data/trending_{datetime.now().strftime('%Y-%m-%d')}.csv"
    pd.DataFrame(keywords, columns=["Keyword"]).to_csv(filename, index=False)
    print(f"✅ Saved {len(keywords)} keywords to {filename}")
else:
    print("⚠️ No keywords found.")
