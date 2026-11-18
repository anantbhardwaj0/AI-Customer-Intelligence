-- 1. Overall Customer Sentiment Summary

SELECT
    sentiment_label,
    COUNT(*) AS total_reviews
FROM customer_reviews
GROUP BY sentiment_label
ORDER BY total_reviews DESC;


-- 2. Customer Satisfaction by Product Rating

SELECT
    rating,
    COUNT(*) AS total_reviews
FROM customer_reviews
GROUP BY rating
ORDER BY rating DESC;


-- 3. Negative Reviews by Product Category

SELECT
    primary_categories,
    COUNT(*) AS negative_reviews
FROM customer_reviews
WHERE sentiment_label = 'Negative'
GROUP BY primary_categories
ORDER BY negative_reviews DESC
LIMIT 10;


-- 4. Most Frequently Discussed Themes

SELECT
    matched_themes,
    COUNT(*) AS total_reviews
FROM customer_reviews
WHERE matched_themes IS NOT NULL
GROUP BY matched_themes
ORDER BY total_reviews DESC
LIMIT 10;


-- 5. Business Recommendations

SELECT
    area,
    finding,
    recommendation
FROM business_recommendations
ORDER BY area;
