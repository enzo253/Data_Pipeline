```markdown
# Bitcoin Prices and Related News - Streamlit Application

## Overview
This project provides a Streamlit web app that allows users to explore Bitcoin price data over time and view related news articles for specific dates. It integrates data from a PostgreSQL database hosted on AWS RDS, where Bitcoin prices and articles are stored. The project also includes an API endpoint for fetching Bitcoin price predictions and related news, and it updates the database **daily at 12 PM** using AWS Lambda.

## Features
- **Bitcoin Price Visualization**: Display historical Bitcoin prices over time using interactive plots.
- **News Articles**: Show related news articles for specific dates.
- **API Integration**: Exposes an API endpoint for users to query Bitcoin price predictions and related news.
- **Daily Updates**: Automatically scrape the latest Bitcoin prices and news **every day at 12 PM** using AWS Lambda and update the database.
- **AWS Deployment**: Host the database on AWS RDS and run scheduled scraping with AWS Lambda.

## Technologies Used
- **Streamlit** → For building the web app.
- **PostgreSQL (AWS RDS)** → For storing Bitcoin prices and related news articles.
- **AWS Lambda** → For automating **daily** scraping and database updates.
- **AWS CloudWatch** → For scheduling Lambda to run **every day at 12 PM**.
- **Plotly** → For generating interactive line plots of Bitcoin prices.
- **psycopg2** → For interacting with the PostgreSQL database in Python.
- **dotenv** → For managing environment variables securely.
- **Requests / BeautifulSoup** → For web scraping Bitcoin news and prices.

---

## Setup and Installation

### Prerequisites
- **Python 3.x** → Ensure Python 3.x is installed on your machine.
- **AWS Account** → You’ll need an AWS account for setting up RDS and Lambda.
- **PostgreSQL Database** → Set up a PostgreSQL database on AWS RDS and get your database connection string.
- **Environment Variables** → Store sensitive credentials (like database credentials) in a `.env` file.

### Install Dependencies

#### 1. Clone the repository:
```sh
git clone https://github.com/yourusername/bitcoin-prices-news.git
cd bitcoin-prices-news
```

#### 2. Create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### 3. Install the required packages:
```sh
pip install -r requirements.txt
```

#### 4. Create a `.env` file in the root directory and add your environment variables:
```
MY_RAILWAY_KEY=your_database_connection_string_here
```

---

## Running the Application Locally
To run the Streamlit app locally, use the following command:
```sh
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501` to view the app.

---

## API Usage
The app exposes an API that can be used to fetch Bitcoin price predictions and related news for a specific date.

### API Endpoint: `/predict`
- **Method**: `GET`

### Request Parameters:
| Parameter | Type  | Description |
|-----------|------|-------------|
| `date` | `string` | The date for which you want to get the Bitcoin price prediction (Format: YYYY-MM-DD). |

### Example Request:
```sh
curl "http://localhost:8501/predict?date=2025-02-01"
```

### Example Response:
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

## Database Schema

### `bitcoin_data` Table (Stores Bitcoin Prices)
| Column  | Type         | Description |
|---------|-------------|-------------|
| `id`    | `SERIAL` (PK) | Unique identifier |
| `date`  | `DATE`        | Date of the recorded price |
| `closing_price` | `FLOAT` | Bitcoin closing price on that date |

### `article_data` Table (Stores News Articles)
| Column  | Type         | Description |
|---------|-------------|-------------|
| `id`    | `SERIAL` (PK) | Unique identifier |
| `title` | `TEXT`       | Article title |
| `link`  | `TEXT`       | Link to the full article |

### `article_bitcoin` Table (Junction Table Linking Bitcoin Data & Articles)
| Column  | Type   | Description |
|---------|--------|-------------|
| `bitcoin_id` | `INT` (FK) | References `bitcoin_data.id` |
| `article_id` | `INT` (FK) | References `article_data.id` |

---

## AWS Deployment

### 1️⃣ AWS Lambda for Daily Updates at 12 PM
- Set up an **AWS Lambda function** that scrapes the latest Bitcoin prices and news articles.
- Configure **AWS CloudWatch Events** to trigger the Lambda function **every day at 12 PM (UTC or your preferred timezone)**.
- Ensure the Lambda function updates the PostgreSQL database on AWS RDS.

### 2️⃣ AWS RDS for Database Storage
- Create an **AWS RDS** instance using **PostgreSQL**.
- Store all Bitcoin price data and related news in the database.
- Ensure security with **IAM roles** and **VPC settings**.

---

## Security Considerations
✅ **Environment Variables**: Store database credentials securely using `.env`.
✅ **AWS IAM Roles**: Use IAM roles to limit database access.
✅ **Database Security**: Restrict RDS access to specific IPs.

---

## Contributing
1. **Fork this repository**.
2. **Create a new branch** for your feature:
   ```sh
   git checkout -b feature-name
   ```
3. **Commit your changes**:
   ```sh
   git commit -am "Add new feature"
   ```
4. **Push to the branch**:
   ```sh
   git push origin feature-name
   ```
5. **Create a new Pull Request**.

---

## License
This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## Contact
📩 **Email:** [enzo.wurtele@outlook.com](mailto:enzo.wurtele@outlook.com)

🚀 Check out the app: [Streamlit Bitcoin News App](https://bitcoinnews-krtk4tzwzgxupivcyjmhxc.streamlit.app/)
```

