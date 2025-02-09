# **Bitcoin Prices and Related News - Streamlit Application**

## Overview

This project provides a **Streamlit web app** that allows users to explore Bitcoin price data over time and view related news articles for specific dates. It integrates data from a **PostgreSQL database** hosted on **AWS RDS**, where Bitcoin prices and articles are stored. The project also includes an API endpoint for fetching Bitcoin price predictions and related news, and it updates the database weekly using **AWS Lambda**.

---

## **Features**

- **Bitcoin Price Visualization**: Display historical Bitcoin prices over time using interactive plots.
- **News Articles**: Show related news articles for specific dates.
- **API Integration**: Exposes an API endpoint for users to query Bitcoin price predictions and related news.
- **Weekly Updates**: Automatically scrape the latest Bitcoin prices and news every week using AWS Lambda and update the database.
- **AWS Deployment**: Host the app and database on **AWS** (Elastic Beanstalk for deployment and RDS for PostgreSQL database).

---

## **Technologies Used**

- **Streamlit**: For building the web app.
- **PostgreSQL**: For storing Bitcoin prices and related news articles.
- **AWS**: For hosting the database (RDS), deploying the app (Elastic Beanstalk), and automating weekly updates (Lambda).
- **Plotly**: For generating interactive line plots of Bitcoin prices.
- **psycopg2**: For interacting with the PostgreSQL database in Python.
- **dotenv**: For managing environment variables securely.
- **Requests / BeautifulSoup**: For web scraping Bitcoin news and prices.

---

## **Setup and Installation**

### **Prerequisites**

1. **Python 3.x**: Ensure Python 3.x is installed on your machine.
2. **AWS Account**: You’ll need an AWS account for setting up RDS, Lambda, and Elastic Beanstalk.
3. **PostgreSQL Database**: Set up a PostgreSQL database on **AWS RDS** and get your database connection string.
4. **Environment Variables**: Store sensitive credentials (like database credentials) in a `.env` file.

### **Install Dependencies**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/bitcoin-prices-news.git
   cd bitcoin-prices-news
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of your project and add your environment variables:

   ```env
   MY_RAILWAY_KEY=your_database_connection_string_here
   ```

---

## **Running the Application Locally**

1. To run the Streamlit app locally, use the following command:

   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501` to view the app.

---

## **API Usage**

The app exposes an API that can be used to fetch Bitcoin price predictions and related news for a specific date.

### **API Endpoint**: `/predict`

**Method**: `GET`

**Request Parameters**:

- `date`: The date for which you want to get the Bitcoin price prediction (Format: `YYYY-MM-DD`).

**Example Request**:

```bash
curl "http://localhost:8501/predict?date=2025-02-01"
```

**Response**:

```json
{
    "date": "2025-02-01",
    "predicted_price": 40000.25,
    "articles": [
        {
            "title": "Bitcoin Reaches New Heights",
            "link": "https://example.com/bitcoin-new-heights"
        },
        {
            "title": "The Future of Cryptocurrency",
            "link": "https://example.com/cryptocurrency-future"
        }
    ]
}
```

---

## **Database**

### **Schema**:

1. **bitcoin_data** table: Stores Bitcoin prices.

   - `id`: Unique identifier (Primary Key)
   - `date`: Date of the recorded price
   - `closing_price`: Bitcoin closing price on that date

2. **article_data** table: Stores news articles.

   - `id`: Unique identifier (Primary Key)
   - `title`: Article title
   - `link`: Link to the full article

3. **article_bitcoin** table: A junction table that links Bitcoin data with related news articles.

   - `bitcoin_id`: Foreign key referencing `bitcoin_data.id`
   - `article_id`: Foreign key referencing `article_data.id`

---

## **AWS Deployment**

### **1. AWS Lambda for Weekly Updates**

1. Set up an **AWS Lambda function** that scrapes the latest Bitcoin prices and news articles from a predefined source.
2. Configure **AWS CloudWatch Events** to trigger the Lambda function weekly.
3. Ensure the Lambda function updates the PostgreSQL database on **AWS RDS**.

### **2. AWS Elastic Beanstalk for App Deployment**

1. Create an **Elastic Beanstalk** application.
2. Deploy the Streamlit app using **Elastic Beanstalk CLI**.

```bash
eb init -p python-3.8 bitcoin-prices-news
eb create bitcoin-prices-env
eb deploy
```

3. Set environment variables (e.g., database connection string) in the **Elastic Beanstalk console**.

---

## **Security Considerations**

- Ensure that your **database connection strings** and **API keys** are stored securely using **environment variables**.
- Use **AWS IAM roles** to control access to the database and other AWS resources.

---

## **Contributing**

1. Fork this repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Contact**

If you have any questions or suggestions, feel free to reach out at [enzo.wurtele@outlook.com].
