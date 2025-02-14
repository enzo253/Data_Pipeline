import requests
import os
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

api_key = os.getenv("MY_API_KEY")

railway_db = os.getenv("MY_RAILWAY_KEY")

print(railway_db)
print(api_key)

def get_bitcoin_data():
    url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo" + api_key
    response_00 = requests.get(url)
    values_00 = response_00.json()

    print(values_00)

    time_series_daily = values_00.get("Time Series (Digital Currency Daily)", {})

    bitcoin_data = []
    for date, data in time_series_daily.items():
        
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        if date_obj > datetime(2024, 8, 1):
            closing_price = data.get("4. close", None) 
            bitcoin_data.append({"Date": date, "Closing_Price": closing_price})
    
    return bitcoin_data

def get_bitcoin_news():
    
    base_url = "https://www.ft.com/search?q=bitcoin&sort=date&page="
    article_data = []
    i = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

    while i < 10:
        url = base_url + str(i)
        response_01 = requests.get(url, headers=headers)

        if response_01.status_code == 200:
            soup = BeautifulSoup(response_01.text, "html.parser")
            articles = soup.find_all("a", class_= "js-teaser-heading-link")
            article_date = soup.find_all("time", class_="o-teaser__timestamp-date")

            for article, date_tag in zip(articles, article_date):
                day = date_tag.get("datetime")
                day = datetime.fromisoformat(day[:10])

                if day > datetime(2024, 8, 1):
                    title = article.text.strip() 
                    day = day.date()
                    link = "https://www.ft.com" + article["href"]
                    article_data.append({"Title": title, "Link": link, "Date": day})

            print(f"✅ Scraped page {i}")
        else:
            print(f"❌ Error: {response_01.status_code} on page {i}")
            break

        i += 1
       
    return article_data

def save_to_railway(bitcoin_data, article_data):

    try:
        conn = psycopg2.connect(railway_db)
        cursor = conn.cursor()

        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS article_bitcoin CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS bitcoin_data CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS article_data CASCADE;")

        # Create tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS article_data (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            date DATE,
            link TEXT
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS bitcoin_data (
            id SERIAL PRIMARY KEY,
            date DATE UNIQUE,
            closing_price NUMERIC
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS article_bitcoin (
            article_id INT REFERENCES article_data(id) ON DELETE CASCADE,
            bitcoin_id INT REFERENCES bitcoin_data(id) ON DELETE CASCADE,
            PRIMARY KEY (article_id, bitcoin_id)
        );''')

        # Insert Articles
        for article in article_data:
            title = article["Title"]
            link = article["Link"]
            date = article["Date"]
            cursor.execute("""
                INSERT INTO article_data (title, link, date)
                VALUES (%s, %s, %s)
                ON CONFLICT (title) DO UPDATE 
                SET link = EXCLUDED.link, date = EXCLUDED.date
                RETURNING id;
            """, (title, link, date))
            article_id = cursor.fetchone()[0]  # Get inserted/updated article ID

            # Find Bitcoin ID for the same date
            cursor.execute("SELECT id FROM bitcoin_data WHERE date = %s;", (date,))
            bitcoin_result = cursor.fetchone()

            if bitcoin_result:
                bitcoin_id = bitcoin_result[0]
                # Link article to bitcoin price
                cursor.execute("""
                    INSERT INTO article_bitcoin (article_id, bitcoin_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (article_id, bitcoin_id))

        # Insert Bitcoin Data
        for item in bitcoin_data:
            date = item["Date"]
            closing_price = item["Closing_Price"]
            cursor.execute("""
                INSERT INTO bitcoin_data (date, closing_price)
                VALUES (%s, %s)
                ON CONFLICT (date) DO UPDATE 
                SET closing_price = EXCLUDED.closing_price
                RETURNING id;
            """, (date, closing_price))
            bitcoin_id = cursor.fetchone()[0]  # Get inserted/updated bitcoin ID

            # Find articles for the same date
            cursor.execute("SELECT id FROM article_data WHERE date = %s;", (date,))
            article_results = cursor.fetchall()

            for article_result in article_results:
                article_id = article_result[0]
                # Link bitcoin price to articles
                cursor.execute("""
                    INSERT INTO article_bitcoin (article_id, bitcoin_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (article_id, bitcoin_id))

        conn.commit()
        cursor.close()
        conn.close()
        print("Data saved successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")


bitcoin_data = get_bitcoin_data()  
news_articles = get_bitcoin_news() 

def main(event, context):
    print("Bitcoin Data:", bitcoin_data)
    print("News Articles:", news_articles)

    if bitcoin_data and news_articles:
        print("Data available, saving to database...")
        save_to_railway(bitcoin_data, news_articles)
    else:
        print("❌ No data available.")

    


    

