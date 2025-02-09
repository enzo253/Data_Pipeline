import streamlit as st
import psycopg2
import pandas as pd
import os 
from dotenv import load_dotenv


load_dotenv()

railway_key = os.getenv("MY_RAILWAY_KEY")

def get_data():

    conn = psycopg2.connect(railway_key)
    cursor = conn.cursor()

    cursor.execute('''SELECT b.date, b.closing_price, a.title, a.link
        FROM bitcoin_data b
        LEFT JOIN article_bitcoin ab ON b.id = ab.bitcoin_id
        LEFT JOIN article_data a ON ab.article_id = a.id
        ORDER BY b.date DESC;
    ''')

    data = cursor.fetchall()
    conn.close()

    return data

info = get_data()

print(info)



