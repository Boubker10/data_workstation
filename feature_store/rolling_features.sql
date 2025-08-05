{{PORTFOLIO_CTE}},
base_data AS (
    SELECT
        p.store,
        p.date,
        w."Weekly_Sales"
    FROM portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
)

SELECT
    *,
    AVG("Weekly_Sales") OVER (
        PARTITION BY store
        ORDER BY TO_DATE(date, 'DD-MM-YYYY')
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS Weekly_Sales_rolling_mean_2,

    STDDEV("Weekly_Sales") OVER (
        PARTITION BY store
        ORDER BY TO_DATE(date, 'DD-MM-YYYY')
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS Weekly_Sales_rolling_std_2,

    AVG("Weekly_Sales") OVER (
        PARTITION BY store
        ORDER BY TO_DATE(date, 'DD-MM-YYYY')
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS Weekly_Sales_rolling_mean_4,

    STDDEV("Weekly_Sales") OVER (
        PARTITION BY store
        ORDER BY TO_DATE(date, 'DD-MM-YYYY')
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS Weekly_Sales_rolling_std_4
FROM base_data
ORDER BY store, TO_DATE(date, 'DD-MM-YYYY');