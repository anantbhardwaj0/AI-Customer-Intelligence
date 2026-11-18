-- 1. Customer Sentiment Summary View

CREATE OR REPLACE VIEW customer_sentiment_summary AS
SELECT
    sentiment_label,
    COUNT(*) AS total_reviews,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_reviews),
        2
    ) AS percentage
FROM customer_reviews
GROUP BY sentiment_label;


-- 2. Product Rating Summary View

CREATE OR REPLACE VIEW product_rating_summary AS
SELECT
    rating,
    COUNT(*) AS total_reviews
FROM customer_reviews
GROUP BY rating;


-- 3. Negative Feedback Summary View

CREATE OR REPLACE VIEW negative_feedback_summary AS
SELECT
    matched_themes AS theme,
    COUNT(*) AS negative_reviews
FROM customer_reviews
WHERE sentiment_label = 'Negative'
GROUP BY matched_themes;


-- 4. Business Recommendations View

CREATE OR REPLACE VIEW business_recommendations_summary AS
SELECT
    area,
    finding,
    recommendation
FROM business_recommendations;
