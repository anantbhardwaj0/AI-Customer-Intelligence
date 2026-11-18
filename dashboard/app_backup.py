
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("AI-Powered Customer Intelligence")
st.subheader("Voice of Customer Analytics Platform")

st.markdown(
    "An interactive dashboard for customer sentiment, "
    "product ratings, feedback themes and business insights."
)


# --------------------------------------------------
# 2. DATABASE CONFIGURATION
# --------------------------------------------------

DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "voc_analytics_db"
DB_USER = "postgres"


@st.cache_resource
def create_database_connection(password):

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=password,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    return create_engine(database_url)


def fetch_data(engine, query):

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)


# --------------------------------------------------
# 3. DATABASE LOGIN
# --------------------------------------------------

st.sidebar.header("Database Connection")

password = st.sidebar.text_input(
    "PostgreSQL Password",
    type="password"
)

if password:

    try:
        engine = create_database_connection(password)

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        st.sidebar.success("Database Connected Successfully!")

        # --------------------------------------------------
        # 4. KPI CARDS
        # --------------------------------------------------

        kpi_data = fetch_data(
            engine,
            """
            SELECT
                COUNT(*) AS total_reviews,
                ROUND(AVG(rating)::numeric, 2) AS average_rating,
                COUNT(*) FILTER (
                    WHERE sentiment_label = 'Positive'
                ) AS positive_reviews,
                COUNT(*) FILTER (
                    WHERE sentiment_label = 'Negative'
                ) AS negative_reviews
            FROM customer_reviews
            """
        )

        total_reviews = int(kpi_data.iloc[0]["total_reviews"])
        average_rating = kpi_data.iloc[0]["average_rating"]
        positive_reviews = int(kpi_data.iloc[0]["positive_reviews"])
        negative_reviews = int(kpi_data.iloc[0]["negative_reviews"])

        st.divider()
        st.header("Customer Analytics Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Reviews", f"{total_reviews:,}")
        col2.metric("Positive Reviews", f"{positive_reviews:,}")
        col3.metric("Negative Reviews", f"{negative_reviews:,}")
        col4.metric("Average Rating", f"{average_rating}/5")

        # --------------------------------------------------
        # 5. SENTIMENT DISTRIBUTION
        # --------------------------------------------------

        sentiment_data = fetch_data(
            engine,
            """
            SELECT
                sentiment_label,
                COUNT(*) AS total_reviews
            FROM customer_reviews
            GROUP BY sentiment_label
            ORDER BY total_reviews DESC
            """
        )

        st.divider()
        st.header("Customer Sentiment Analysis")

        st.bar_chart(
            sentiment_data.set_index("sentiment_label"),
            y="total_reviews"
        )

        st.dataframe(
            sentiment_data,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # 6. PRODUCT RATING DISTRIBUTION
        # --------------------------------------------------

        rating_data = fetch_data(
            engine,
            """
            SELECT
                rating,
                COUNT(*) AS total_reviews
            FROM customer_reviews
            GROUP BY rating
            ORDER BY rating
            """
        )

        st.divider()
        st.header("Product Rating Distribution")

        st.bar_chart(
            rating_data.set_index("rating"),
            y="total_reviews"
        )

        # --------------------------------------------------
        # 7. CUSTOMER FEEDBACK THEMES
        # --------------------------------------------------

        theme_data = fetch_data(
            engine,
            """
            SELECT
                TRIM(t.theme) AS theme,
                COUNT(*) AS total_reviews
            FROM customer_reviews AS cr
            CROSS JOIN LATERAL
                UNNEST(STRING_TO_ARRAY(cr.matched_themes, ';'))
                AS t(theme)
            WHERE cr.matched_themes IS NOT NULL
              AND TRIM(t.theme) <> ''
            GROUP BY TRIM(t.theme)
            ORDER BY total_reviews DESC
            """
        )

        st.divider()
        st.header("Customer Feedback Theme Analysis")

        st.bar_chart(
            theme_data.set_index("theme"),
            y="total_reviews"
        )

        st.dataframe(
            theme_data,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # 8. NEGATIVE FEEDBACK ANALYSIS
        # --------------------------------------------------

        negative_data = fetch_data(
            engine,
            """
            SELECT
                TRIM(t.theme) AS theme,
                COUNT(*) AS negative_reviews
            FROM customer_reviews AS cr
            CROSS JOIN LATERAL
                UNNEST(STRING_TO_ARRAY(cr.matched_themes, ';'))
                AS t(theme)
            WHERE cr.sentiment_label = 'Negative'
              AND cr.matched_themes IS NOT NULL
              AND TRIM(t.theme) <> ''
            GROUP BY TRIM(t.theme)
            ORDER BY negative_reviews DESC
            """
        )

        st.divider()
        st.header("Negative Customer Feedback Analysis")

        st.bar_chart(
            negative_data.set_index("theme"),
            y="negative_reviews"
        )

        st.dataframe(
            negative_data,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # 9. BUSINESS RECOMMENDATIONS
        # --------------------------------------------------

        recommendations_data = fetch_data(
            engine,
            """
            SELECT area, finding, recommendation
            FROM business_recommendations
            ORDER BY recommendation_id
            """
        )

        st.divider()
        st.header("Business Recommendations")

        st.dataframe(
            recommendations_data,
            use_container_width=True,
            hide_index=True
        )

        st.success("Dashboard Data Loaded Successfully!")

    except Exception as error:
        st.sidebar.error("Database Connection or Query Failed")
        st.error(f"Error Details: {error}")

else:
    st.info(
        "Please enter your PostgreSQL password in the sidebar "
        "to load the dashboard."
    )


# --------------------------------------------------
# 10. DASHBOARD FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Powered Customer Intelligence and Voice of Customer Analytics Platform"
)
