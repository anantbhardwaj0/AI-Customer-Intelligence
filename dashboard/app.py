import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text


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
# 2. DATABASE CONNECTION
# --------------------------------------------------

@st.cache_resource
def create_database_connection(database_url):
    return create_engine(
        database_url,
        pool_pre_ping=True
    )


def fetch_data(engine, query, params=None):
    with engine.connect() as connection:
        return pd.read_sql(
            text(query),
            connection,
            params=params
        )


# --------------------------------------------------
# 3. DATABASE LOGIN
# --------------------------------------------------

st.sidebar.header("Database Connection")

try:

    database_url = st.secrets["connections"]["postgresql"]["url"]

    engine = create_database_connection(database_url)

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    st.sidebar.success("Database Connected Successfully!")

except Exception as error:

    st.sidebar.error("Database Connection Failed")

    st.error(
        "Unable to connect to the database. "
        "Please check your Streamlit Cloud Secrets."
    )

    st.stop()


# --------------------------------------------------
# 4. INTERACTIVE DASHBOARD FILTERS
# --------------------------------------------------

try:

    st.sidebar.divider()
    st.sidebar.header("Dashboard Filters")

    # Product category filter

    category_data = fetch_data(
        engine,
        """
        SELECT DISTINCT categories
        FROM public.customer_reviews
        WHERE categories IS NOT NULL
          AND TRIM(categories) <> ''
        ORDER BY categories
        """
    )

    category_options = (
        ["All"] + category_data["categories"].tolist()
    )

    selected_category = st.sidebar.selectbox(
        "Product Category",
        options=category_options
    )

    # Sentiment filter

    sentiment_options = ["Positive", "Neutral", "Negative"]

    selected_sentiments = st.sidebar.multiselect(
        "Sentiment",
        options=sentiment_options,
        default=sentiment_options
    )

    # Rating filter

    rating_options = ["All", 1, 2, 3, 4, 5]

    selected_rating = st.sidebar.selectbox(
        "Product Rating",
        options=rating_options
    )

    # SQL filter conditions

    filter_params = {}
    filter_conditions = []

    if selected_category != "All":

        filter_conditions.append(
            "categories = :category"
        )

        filter_params["category"] = selected_category

    if selected_sentiments != sentiment_options:

        if selected_sentiments:

            filter_conditions.append(
                "sentiment_label = ANY(CAST(:sentiments AS text[]))"
            )

            filter_params["sentiments"] = selected_sentiments

        else:

            filter_conditions.append("1 = 0")

    if selected_rating != "All":

        filter_conditions.append(
            "rating = :rating"
        )

        filter_params["rating"] = selected_rating

    # Reusable WHERE clause

    def make_where_clause(table_alias=""):

        prefix = f"{table_alias}." if table_alias else ""

        conditions = []

        if selected_category != "All":

            conditions.append(
                f"{prefix}categories = :category"
            )

        if selected_sentiments != sentiment_options:

            if selected_sentiments:

                conditions.append(
                    f"{prefix}sentiment_label = "
                    "ANY(CAST(:sentiments AS text[]))"
                )

            else:

                conditions.append("1 = 0")

        if selected_rating != "All":

            conditions.append(
                f"{prefix}rating = :rating"
            )

        return (
            " WHERE " + " AND ".join(conditions)
            if conditions else ""
        )

    where_clause = make_where_clause()

    theme_where_clause = make_where_clause("cr")

    st.sidebar.caption(
        "Change filters to update the dashboard."
    )


    # --------------------------------------------------
    # 5. KPI CARDS
    # --------------------------------------------------

    kpi_data = fetch_data(
        engine,
        f"""
        SELECT
            COUNT(*) AS total_reviews,

            ROUND(AVG(rating)::numeric, 2)
                AS average_rating,

            COUNT(*) FILTER (
                WHERE sentiment_label = 'Positive'
            ) AS positive_reviews,

            COUNT(*) FILTER (
                WHERE sentiment_label = 'Negative'
            ) AS negative_reviews

        FROM public.customer_reviews

        {where_clause}
        """,
        filter_params
    )

    total_reviews = int(
        kpi_data.iloc[0]["total_reviews"]
    )

    average_rating = (
        kpi_data.iloc[0]["average_rating"]
    )

    positive_reviews = int(
        kpi_data.iloc[0]["positive_reviews"]
    )

    negative_reviews = int(
        kpi_data.iloc[0]["negative_reviews"]
    )

    st.divider()
    st.header("Customer Analytics Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Reviews",
        f"{total_reviews:,}"
    )

    col2.metric(
        "Positive Reviews",
        f"{positive_reviews:,}"
    )

    col3.metric(
        "Negative Reviews",
        f"{negative_reviews:,}"
    )

    col4.metric(
        "Average Rating",
        f"{average_rating}/5"
        if pd.notna(average_rating)
        else "N/A"
    )


    # --------------------------------------------------
    # 6. SENTIMENT DISTRIBUTION
    # --------------------------------------------------

    sentiment_data = fetch_data(
        engine,
        f"""
        SELECT
            sentiment_label,
            COUNT(*) AS total_reviews

        FROM public.customer_reviews

        {where_clause}

        GROUP BY sentiment_label

        ORDER BY total_reviews DESC
        """,
        filter_params
    )

    st.divider()
    st.header("Customer Sentiment Analysis")

    if not sentiment_data.empty:

        st.bar_chart(
            sentiment_data.set_index("sentiment_label"),
            y="total_reviews"
        )

        st.dataframe(
            sentiment_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sentiment data is available for the selected filters."
        )


    # --------------------------------------------------
    # 7. PRODUCT RATING DISTRIBUTION
    # --------------------------------------------------

    rating_data = fetch_data(
        engine,
        f"""
        SELECT
            rating,
            COUNT(*) AS total_reviews

        FROM public.customer_reviews

        {where_clause}

        GROUP BY rating

        ORDER BY rating
        """,
        filter_params
    )

    st.divider()
    st.header("Product Rating Distribution")

    if not rating_data.empty:

        st.bar_chart(
            rating_data.set_index("rating"),
            y="total_reviews"
        )

        st.dataframe(
            rating_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No rating data is available for the selected filters."
        )


    # --------------------------------------------------
    # 8. CUSTOMER FEEDBACK THEMES
    # --------------------------------------------------

    theme_data = fetch_data(
        engine,
        f"""
        SELECT
            TRIM(t.theme) AS theme,
            COUNT(*) AS total_reviews

        FROM public.customer_reviews AS cr

        CROSS JOIN LATERAL
            UNNEST(
                STRING_TO_ARRAY(cr.matched_themes, ';')
            ) AS t(theme)

        {theme_where_clause}

        {"AND" if theme_where_clause else "WHERE"}
            cr.matched_themes IS NOT NULL
            AND TRIM(t.theme) <> ''

        GROUP BY TRIM(t.theme)

        ORDER BY total_reviews DESC
        """,
        filter_params
    )

    st.divider()
    st.header("Customer Feedback Theme Analysis")

    if not theme_data.empty:

        st.bar_chart(
            theme_data.set_index("theme"),
            y="total_reviews"
        )

        st.dataframe(
            theme_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No theme data is available for the selected filters."
        )


    # --------------------------------------------------
    # 9. NEGATIVE FEEDBACK ANALYSIS
    # --------------------------------------------------

    negative_theme_conditions = []

    if selected_category != "All":

        negative_theme_conditions.append(
            "cr.categories = :category"
        )

    if selected_rating != "All":

        negative_theme_conditions.append(
            "cr.rating = :rating"
        )

    if "Negative" in selected_sentiments:

        negative_theme_conditions.append(
            "cr.sentiment_label = 'Negative'"
        )

    else:

        negative_theme_conditions.append("1 = 0")

    negative_theme_where = (
        " WHERE " + " AND ".join(negative_theme_conditions)
    )

    negative_data = fetch_data(
        engine,
        f"""
        SELECT
            TRIM(t.theme) AS theme,
            COUNT(*) AS negative_reviews

        FROM public.customer_reviews AS cr

        CROSS JOIN LATERAL
            UNNEST(
                STRING_TO_ARRAY(cr.matched_themes, ';')
            ) AS t(theme)

        {negative_theme_where}

        AND cr.matched_themes IS NOT NULL
        AND TRIM(t.theme) <> ''

        GROUP BY TRIM(t.theme)

        ORDER BY negative_reviews DESC
        """,
        filter_params
    )

    st.divider()
    st.header("Negative Customer Feedback Analysis")

    if not negative_data.empty:

        st.bar_chart(
            negative_data.set_index("theme"),
            y="negative_reviews"
        )

        st.dataframe(
            negative_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No negative feedback is available for the selected filters."
        )


    # --------------------------------------------------
    # 10. FILTERED CUSTOMER REVIEWS
    # --------------------------------------------------

    review_data = fetch_data(
        engine,
        f"""
        SELECT
            product_name,
            rating,
            sentiment_label,
            review_text_clean,
            review_date_clean

        FROM public.customer_reviews

        {where_clause}

        ORDER BY review_date_clean DESC NULLS LAST

        LIMIT 100
        """,
        filter_params
    )

    st.divider()
    st.header("Customer Reviews")

    st.caption(
        "Showing up to 100 reviews matching the selected filters."
    )

    st.dataframe(
        review_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # 11. BUSINESS RECOMMENDATIONS
    # --------------------------------------------------

    recommendations_data = fetch_data(
        engine,
        """
        SELECT
            area,
            finding,
            recommendation

        FROM public.business_recommendations

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

    st.success(
        "Dashboard Data Loaded Successfully!"
    )


except Exception as error:

    st.sidebar.error(
        "Database Connection or Query Failed"
    )

    st.error(
        f"Error Details: {error}"
    )


# --------------------------------------------------
# 12. DASHBOARD FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI-Powered Customer Intelligence and Voice of Customer Analytics Platform"
)
