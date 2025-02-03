import streamlit as st
from dotenv import load_dotenv
import requests
import os


load_dotenv()

# Now you can access the API key like this:
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=" + api_key
    response = requests.get(url)
    values = response.json()
    print(values)
    return values



