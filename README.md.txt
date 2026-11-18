# AI-Powered Customer Intelligence & Voice of Customer Analytics

An end-to-end customer feedback analytics platform that transforms unstructured customer reviews into actionable business insights using Python, Natural Language Processing (NLP), Sentiment Analysis, PostgreSQL, and Streamlit.

## Overview

Understanding customer opinions is essential for improving products, services, and customer experience. However, analysing thousands of customer reviews manually is time-consuming and makes it difficult to identify recurring issues and customer satisfaction patterns.

This project provides an analytical solution that processes customer reviews, identifies sentiment, extracts recurring feedback themes, and presents meaningful insights through an interactive dashboard.

The platform combines data processing, NLP-based sentiment analysis, theme identification, SQL analytics, and interactive visualization into one workflow.

## Key Features

- **Exploratory Data Analysis:** Understand customer review patterns, ratings, categories, and data quality.
- **Data Cleaning:** Handle missing values, validate dates, and prepare review text for analysis.
- **Sentiment Analysis:** Classify customer reviews as Positive, Negative, or Neutral using VADER.
- **Theme Analysis:** Identify recurring feedback topics using keyword-based classification.
- **Customer Intelligence:** Analyse customer satisfaction across product categories, ratings, and feedback themes.
- **Database Integration:** Store analytical results in PostgreSQL and generate insights using SQL queries and views.
- **Interactive Dashboard:** Explore KPIs, sentiment distribution, ratings, themes, and filtered customer reviews using Streamlit.
- **Business Recommendations:** Translate analytical findings into practical recommendations.

## Technology Stack

| Category | Tools |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| NLP | NLTK, VADER |
| Database | PostgreSQL |
| Database Connectivity | SQLAlchemy, Psycopg2 |
| Dashboard | Streamlit |
| Development Environment | Jupyter Notebook |
| Version Control | Git, GitHub |

## Dataset

The project uses a consumer product reviews dataset containing customer feedback, product information, ratings, and review-related attributes.

| Metric | Value |
|---|---:|
| Total Reviews | 28,332 |
| Original Columns | 24 |
| Final Analysis Columns | 30 |
| Duplicate Records | 0 |
| Average Rating | 4.51 / 5 |

The raw dataset is not included in the repository because of its large file size.

## Analytical Methodology

The project follows an end-to-end analytics workflow:

1. Data loading and exploration.
2. Data quality assessment and preprocessing.
3. Customer review text cleaning.
4. VADER-based sentiment scoring and classification.
5. Keyword-based customer feedback theme identification.
6. Sentiment and theme analysis.
7. Final business insights and recommendations.
8. PostgreSQL database integration.
9. Interactive Streamlit dashboard development.

## Key Results

### Sentiment Distribution

| Sentiment | Reviews | Percentage |
|---|---:|---:|
| Positive | 23,724 | 83.74% |
| Neutral | 2,498 | 8.82% |
| Negative | 2,110 | 7.45% |

### Business Insights

- **Average Customer Rating:** 4.51 out of 5.
- **Most Discussed Identified Theme:** Price and Value.
- **Highest Negative Sentiment Percentage Among Identified Themes:** Customer Service (12.12%).
- **Highest Negative Feedback Rate Among Major Product Categories:** Health & Beauty (9.34%).

These insights help identify customer experience gaps and areas that may require business improvement.

## Database

**Database:** `voc_analytics_db`

### Main Tables

- `customer_reviews` — stores customer review records, ratings, sentiment results, and identified themes.
- `business_recommendations` — stores analytical findings and recommendations.

### SQL Views

- `customer_sentiment_summary`
- `product_rating_summary`
- `negative_feedback_summary`
- `business_recommendations_summary`

Database scripts are available in the `sql/` directory.

## Project Structure

```text
AI_Customer_Intelligence/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Sentiment_Analysis.ipynb
│   ├── 04_Theme_Analysis.ipynb
│   ├── 05_Final_Analysis.ipynb
│   └── 06_Database_Integration.ipynb
│
├── reports/
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_data_analysis_queries.sql
│   ├── 03_business_insights.sql
│   └── 04_views.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Customer-Intelligence.git
```

### 2. Navigate to the Project

```bash
cd AI-Customer-Intelligence
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

- Start PostgreSQL.
- Create a database named `voc_analytics_db`.
- Execute the SQL scripts from the `sql/` directory.
- Import the processed customer data and recommendations.
- Configure database credentials using environment variables or Streamlit secrets.

### 5. Launch the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

Open the local URL provided by Streamlit, usually:

`http://localhost:8501`

## Limitations and Future Enhancements

- Introduce transformer-based models such as BERT for contextual sentiment analysis.
- Explore LDA or BERTopic for automated topic discovery.
- Improve theme classification beyond predefined keywords.
- Implement aspect-based sentiment analysis.
- Integrate real-time customer feedback sources.
- Add automated reporting and cloud deployment.

## Notes

- Sentiment classification currently uses VADER.
- Theme identification currently uses predefined keyword-based rules.
- The raw dataset and database credentials are excluded from the repository.
- A running PostgreSQL database with the required tables is necessary to use the dashboard.

---

**Built with Python, NLP, PostgreSQL, and Streamlit.**