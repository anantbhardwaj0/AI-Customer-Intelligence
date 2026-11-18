-- 1. Sentiment Distribution

SELECT
    sentiment_label,
    COUNT(*) AS total_reviews,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_reviews),
        2
    ) AS percentage
FROM customer_reviews
GROUP BY sentiment_label
ORDER BY total_reviews DESC;


-- 2. Average Product Rating

SELECT
    ROUND(AVG(rating)::NUMERIC, 2) AS average_rating
FROM customer_reviews;


-- 3. Rating-wise Distribution

SELECT
    rating,
    COUNT(*) AS total_reviews,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_reviews),
        2
    ) AS percentage
FROM customer_reviews
GROUP BY rating
ORDER BY rating;


-- 4. Customer Feedback Theme Distribution

SELECT
    matched_themes AS theme,
    COUNT(*) AS total_reviews
FROM customer_reviews
WHERE matched_themes IS NOT NULL
AND TRIM(matched_themes) != ''
GROUP BY matched_themes
ORDER BY total_reviews DESC;


-- 5. Negative Feedback by Theme

SELECT
    matched_themes AS theme,
    COUNT(*) AS negative_reviews
FROM customer_reviews
WHERE sentiment_label = 'Negative'
GROUP BY matched_themes
ORDER BY negative_reviews DESC;


-- 6. Total Customer Reviews

SELECT COUNT(*) AS total_reviews
FROM customer_reviews;


-- 7. Business Recommendations

SELECT *
FROM business_recommendations;
