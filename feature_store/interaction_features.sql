{{PORTFOLIO_CTE}},
base_data AS (
    SELECT 
        p.store,
        p.date,
        w."Fuel_Price",
        w."Unemployment",
        w."CPI",
        w."Temperature",
        w."Holiday_Flag",
        -- Calcul direct des flags d'événements (fenêtre +/- 7 jours)
        CASE WHEN EXISTS (
            SELECT 1 FROM (VALUES 
                (DATE '2010-02-12'), (DATE '2011-02-11'), (DATE '2012-02-10'), (DATE '2013-02-08')
            ) AS sb(event_date) 
            WHERE ABS(TO_DATE(p.date, 'DD-MM-YYYY') - sb.event_date) <= 7
        ) THEN 1 ELSE 0 END AS super_bowl_flag,
        
        CASE WHEN EXISTS (
            SELECT 1 FROM (VALUES 
                (DATE '2010-09-10'), (DATE '2011-09-09'), (DATE '2012-09-07'), (DATE '2013-09-06')
            ) AS ld(event_date) 
            WHERE ABS(TO_DATE(p.date, 'DD-MM-YYYY') - ld.event_date) <= 7
        ) THEN 1 ELSE 0 END AS labour_day_flag,
        
        CASE WHEN EXISTS (
            SELECT 1 FROM (VALUES 
                (DATE '2010-11-26'), (DATE '2011-11-25'), (DATE '2012-11-23'), (DATE '2013-11-29')
            ) AS th(event_date) 
            WHERE ABS(TO_DATE(p.date, 'DD-MM-YYYY') - th.event_date) <= 7
        ) THEN 1 ELSE 0 END AS thanksgiving_flag,
        
        CASE WHEN EXISTS (
            SELECT 1 FROM (VALUES 
                (DATE '2010-12-31'), (DATE '2011-12-30'), (DATE '2012-12-28'), (DATE '2013-12-27')
            ) AS ch(event_date) 
            WHERE ABS(TO_DATE(p.date, 'DD-MM-YYYY') - ch.event_date) <= 7
        ) THEN 1 ELSE 0 END AS christmas_flag,
        -- Calcul de la saison à partir de la date
        CASE 
            WHEN EXTRACT(MONTH FROM TO_DATE(p.date, 'DD-MM-YYYY')) IN (3,4,5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM TO_DATE(p.date, 'DD-MM-YYYY')) IN (6,7,8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM TO_DATE(p.date, 'DD-MM-YYYY')) IN (9,10,11) THEN 'Autumn'
            ELSE 'Winter'
        END AS season
    FROM portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
)

SELECT 
    *,
    "Fuel_Price" * "Unemployment" AS fuel_price_x_unemployment,
    "CPI" * "Unemployment" AS cpi_x_unemployment,
    (("Temperature" - 32) * 5.0 / 9.0) *
    CASE season
        WHEN 'Winter' THEN 0
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Autumn' THEN 3
        ELSE NULL
    END AS temp_x_season,
    "Holiday_Flag"::int * "Fuel_Price" AS holiday_x_fuel_price,
    "Holiday_Flag"::int * (("Temperature" - 32) * 5.0 / 9.0) AS holiday_x_temperature,
    (super_bowl_flag + labour_day_flag + thanksgiving_flag + christmas_flag) AS total_holidays
FROM base_data
ORDER BY store, date;