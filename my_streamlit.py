import streamlit as st
from dotenv import load_dotenv
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

load_dotenv()

# Now you can access the API key like this:
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=" + api_key
    response = requests.get(url)
    values = response.json()
    print(values)
    return values

import requests

def get_closing_prices(api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract daily time series data
    time_series = data.get("Time Series (Daily)", {})

    # Store closing prices in a list
    closing_prices = []
    for date, values in time_series.items():
        closing_price = values.get("4. close")  # Extract closing price
        closing_prices.append({"Date": date, "Closing Price": float(closing_price)})

    # Sort by date (newest first)
    closing_prices.sort(key=lambda x: x["Date"], reverse=True)

    return closing_prices

st.title("📈 IBM Closing Prices")

api_key = "your_api_key_here"
closing_prices = get_closing_prices(api_key)

# Convert to DataFrame for Streamlit
df = pd.DataFrame(closing_prices)

# Display in a table
st.dataframe(df)

# Show as a line chart
st.line_chart(df.set_index("Date"))


# Example usage
api_key = "your_api_key_here"
closing_prices = get_closing_prices(api_key)
print(closing_prices)  # Print the closing prices


# Set up Streamlit UI
st.title("🔎 FT.com Bitcoin News Scraper")
st.write("Fetching latest articles... Please wait.")

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Open FT.com search page
url = "https://www.ft.com/search?q=bitcoin&sort=relevance&isFirstView=true&dateRange=now-24h"
driver.get(url)

# Wait for the articles to load
time.sleep(5)  # You can replace this with WebDriverWait

# Get the page source after JavaScript loads
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all articles
articles = soup.find_all("div", class_="o-teaser")

# Extract article titles & links
data = []
for article in articles:
    title_element = article.find("a")
    img_element = article.find("img")
    if title_element:
        title = title_element.text.strip()
        link = title_element["href"]
        image = img_element["src"]
        if not link.startswith("http"):  # Fix relative links
            link = "https://www.ft.com" + link
        data.append({"Title": title, "Link": link, "Image": image})

# Close Selenium
driver.quit()

# Show results in Streamlit
if data:
    st.success(f"✅ Found {len(data)} articles!")
    for article in data:
        st.markdown(f"🔗 [{article['Title']}]({article['Link']})")  # Clickable links
        st.image(article["Image"], caption=article["Title"], use_column_width=True)
else:
    st.warning("⚠️ No articles found.")