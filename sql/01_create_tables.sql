-- Customer Reviews Table

CREATE TABLE IF NOT EXISTS customer_reviews (
    review_id BIGSERIAL PRIMARY KEY,
    product_id TEXT,
    date_added TEXT,
    date_updated TEXT,
    product_name TEXT,
    asins TEXT,
    brand TEXT,
    categories TEXT,
    primary_categories TEXT,
    image_urls TEXT,
    keys TEXT,
    manufacturer TEXT,
    manufacturer_number TEXT,
    review_date_original TEXT,
    review_date_seen TEXT,
    do_recommend TEXT,
    num_helpful DOUBLE PRECISION,
    rating INTEGER,
    review_source_urls TEXT,
    review_text TEXT,
    review_title TEXT,
    review_username TEXT,
    source_urls TEXT,
    review_text_clean TEXT,
    review_date_clean TEXT,
    vader_negative DOUBLE PRECISION,
    vader_neutral DOUBLE PRECISION,
    vader_positive DOUBLE PRECISION,
    sentiment_score DOUBLE PRECISION,
    sentiment_label TEXT,
    matched_themes TEXT
);

-- Business Recommendations Table

CREATE TABLE IF NOT EXISTS business_recommendations (
    recommendation_id BIGSERIAL PRIMARY KEY,
    area TEXT,
    finding TEXT,
    recommendation TEXT
);
