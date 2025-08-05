{{PORTFOLIO_CTE}},
base_data AS (
    SELECT
        p.store,
        p.date,
        w."Weekly_Sales"
    FROM
        portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
)

SELECT
    *,
    "Weekly_Sales" - LAG("Weekly_Sales") OVER (PARTITION BY store ORDER BY date) AS Weekly_Sales_diff,
    CASE
        WHEN LAG("Weekly_Sales") OVER (PARTITION BY store ORDER BY date) = 0 THEN NULL
        ELSE ("Weekly_Sales" - LAG("Weekly_Sales") OVER (PARTITION BY store ORDER BY date)) / LAG("Weekly_Sales") OVER (PARTITION BY store ORDER BY date)
    END AS Weekly_Sales_pct_change
FROM base_data
ORDER BY store, date;
