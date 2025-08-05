-- Description : Ajoute des features basées sur la date (saison, jour de la semaine, etc.)
-- Entrées requises : 
--    - table temporaire filtered_data avec colonnes Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment
-- Résultat : filtered_data + colonnes month, season, day_of_week, week_of_year, quarter, is_month_start, is_month_end, is_quarter_start, is_quarter_end

WITH filtered_data AS (
    -- ici appeler ou référencer 01_filtered_data.sql
    SELECT * FROM filtered_data -- placeholder, à remplacer par la source
)

SELECT
    *,
    EXTRACT(MONTH FROM Date) AS month,
    CASE
        WHEN EXTRACT(MONTH FROM Date) IN (3,4,5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM Date) IN (6,7,8) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM Date) IN (9,10,11) THEN 'Autumn'
        ELSE 'Winter'
    END AS season,
    EXTRACT(DOW FROM Date) AS day_of_week,
    EXTRACT(WEEK FROM Date) AS week_of_year,
    EXTRACT(QUARTER FROM Date) AS quarter,
    CASE WHEN Date = date_trunc('month', Date) THEN 1 ELSE 0 END AS is_month_start,
    CASE WHEN Date = (date_trunc('month', Date) + INTERVAL '1 month - 1 day')::date THEN 1 ELSE 0 END AS is_month_end,
    CASE WHEN Date = date_trunc('quarter', Date) THEN 1 ELSE 0 END AS is_quarter_start,
    CASE WHEN Date = (date_trunc('quarter', Date) + INTERVAL '3 month - 1 day')::date THEN 1 ELSE 0 END AS is_quarter_end
FROM filtered_data
ORDER BY Store, Date;
