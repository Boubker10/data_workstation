-- Description : Ajout des flags proches des événements importants (fenêtre +/- 7 jours)
-- Entrées requises :
--    - table temporaire avec colonnes Store, Date
-- Résultat : Ajoute les colonnes Super_Bowl_flag, Labour_Day_flag, Thanksgiving_flag, Christmas_flag

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
        -- Ajoutez ici les autres colonnes dont vous avez besoin des étapes précédentes
    FROM portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
),

events AS (
    SELECT 'Super_Bowl' AS event_name, DATE '2010-02-12' AS event_date UNION ALL
    SELECT 'Super_Bowl', DATE '2011-02-11' UNION ALL
    SELECT 'Super_Bowl', DATE '2012-02-10' UNION ALL
    SELECT 'Super_Bowl', DATE '2013-02-08' UNION ALL
    SELECT 'Labour_Day', DATE '2010-09-10' UNION ALL
    SELECT 'Labour_Day', DATE '2011-09-09' UNION ALL
    SELECT 'Labour_Day', DATE '2012-09-07' UNION ALL
    SELECT 'Labour_Day', DATE '2013-09-06' UNION ALL
    SELECT 'Thanksgiving', DATE '2010-11-26' UNION ALL
    SELECT 'Thanksgiving', DATE '2011-11-25' UNION ALL
    SELECT 'Thanksgiving', DATE '2012-11-23' UNION ALL
    SELECT 'Thanksgiving', DATE '2013-11-29' UNION ALL
    SELECT 'Christmas', DATE '2010-12-31' UNION ALL
    SELECT 'Christmas', DATE '2011-12-30' UNION ALL
    SELECT 'Christmas', DATE '2012-12-28' UNION ALL
    SELECT 'Christmas', DATE '2013-12-27'
),

flagged_data AS (
    SELECT d.*,
           MAX(CASE WHEN e.event_name = 'Super_Bowl' AND ABS(TO_DATE(d.Date, 'DD-MM-YYYY') - e.event_date) <= 7 THEN 1 ELSE 0 END) AS Super_Bowl_flag,
           MAX(CASE WHEN e.event_name = 'Labour_Day' AND ABS(TO_DATE(d.Date, 'DD-MM-YYYY') - e.event_date) <= 7 THEN 1 ELSE 0 END) AS Labour_Day_flag,
           MAX(CASE WHEN e.event_name = 'Thanksgiving' AND ABS(TO_DATE(d.Date, 'DD-MM-YYYY') - e.event_date) <= 7 THEN 1 ELSE 0 END) AS Thanksgiving_flag,
           MAX(CASE WHEN e.event_name = 'Christmas' AND ABS(TO_DATE(d.Date, 'DD-MM-YYYY') - e.event_date) <= 7 THEN 1 ELSE 0 END) AS Christmas_flag
    FROM base_data d
    LEFT JOIN events e ON ABS(TO_DATE(d.Date, 'DD-MM-YYYY') - e.event_date) <= 7
    GROUP BY d.Store, d.Date, d."Weekly_Sales", d."Holiday_Flag", d."Temperature", d."Fuel_Price", d."CPI", d."Unemployment"
)

SELECT * FROM flagged_data
ORDER BY Store, Date;