{{PORTFOLIO_CTE}}, 
base_data AS (
    SELECT 
        p.store AS Store,
        p.date AS Date,
        w."Weekly_Sales",
        w."Holiday_Flag",
        w."Temperature",
        w."Fuel_Price",
        w."CPI",
        w."Unemployment"
    FROM portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
)

SELECT 
    *,
    EXTRACT(MONTH FROM TO_DATE(Date, 'DD-MM-YYYY')) AS month,
    CASE 
        WHEN EXTRACT(MONTH FROM TO_DATE(Date, 'DD-MM-YYYY')) IN (3,4,5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM TO_DATE(Date, 'DD-MM-YYYY')) IN (6,7,8) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM TO_DATE(Date, 'DD-MM-YYYY')) IN (9,10,11) THEN 'Autumn'
        ELSE 'Winter'
    END AS season,
    EXTRACT(DOW FROM TO_DATE(Date, 'DD-MM-YYYY')) AS day_of_week,
    EXTRACT(WEEK FROM TO_DATE(Date, 'DD-MM-YYYY')) AS week_of_year,
    EXTRACT(QUARTER FROM TO_DATE(Date, 'DD-MM-YYYY')) AS quarter,
    CASE WHEN TO_DATE(Date, 'DD-MM-YYYY') = date_trunc('month', TO_DATE(Date, 'DD-MM-YYYY')) THEN 1 ELSE 0 END AS is_month_start,
    CASE WHEN TO_DATE(Date, 'DD-MM-YYYY') = (date_trunc('month', TO_DATE(Date, 'DD-MM-YYYY')) + INTERVAL '1 month - 1 day')::date THEN 1 ELSE 0 END AS is_month_end,
    CASE WHEN TO_DATE(Date, 'DD-MM-YYYY') = date_trunc('quarter', TO_DATE(Date, 'DD-MM-YYYY')) THEN 1 ELSE 0 END AS is_quarter_start,
    CASE WHEN TO_DATE(Date, 'DD-MM-YYYY') = (date_trunc('quarter', TO_DATE(Date, 'DD-MM-YYYY')) + INTERVAL '3 month - 1 day')::date THEN 1 ELSE 0 END AS is_quarter_end
FROM base_data
ORDER BY Store, Date;