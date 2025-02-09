import streamlit as st
import psycopg2
import pandas as pd
import os 
from dotenv import load_dotenv
import plotly.express as px


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

    print(data)

    return data


data = get_data()

bitcoin_df = pd.DataFrame(data, columns=["Date", "Closing Price", "Title", "Link"])
bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])

st.title = ("📈 Bitcoin Prices and Related News")


fig = px.line(bitcoin_df, x="Date", y="Closing Price", markers=True, title="Bitcoin Prices Over Time")


selected_date = st.selectbox("Select a Date:", bitcoin_df["Date"].unique())


articles_on_date = bitcoin_df[bitcoin_df["Date"] == selected_date]


st.plotly_chart(fig, use_container_width=True)


st.subheader(f"📰 News Articles for {selected_date.date()}")

for index, row in articles_on_date.iterrows():
    st.markdown(f"### [{row['Title']}]({row['Link']})")

st.subheader("📰 Browse All Articles")

for index, row in bitcoin_df.iterrows():
    with st.expander(f"{row['Date'].date()} - {row['Title']}"):
        st.markdown(f"[Read More]({row['Link']})")



