base_data AS (
    SELECT
        p.store,
        p.date,
        w."Fuel_Price",
        w."Unemployment",
        w."CPI",
        w."Temperature",
        w."Holiday_Flag",
        w."super_bowl_flag",   
        w."labour_day_flag",
        w."thanksgiving_flag",
        w."christmas_flag",
        w."season"
    FROM
        portfolio p
    JOIN walmart w ON w."Store" = p.store AND w."Date" = p.date
)

SELECT
    *,
    Fuel_Price * Unemployment AS fuel_price_x_unemployment,
    CPI * Unemployment AS cpi_x_unemployment,
    ((Temperature - 32) * 5.0 / 9.0) *  -- conversion Fahrenheit -> Celsius
    CASE season
        WHEN 'Winter' THEN 0
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Autumn' THEN 3
        ELSE NULL
    END AS temp_x_season,
    Holiday_Flag * Fuel_Price AS holiday_x_fuel_price,
    Holiday_Flag * ((Temperature - 32) * 5.0 / 9.0) AS holiday_x_temperature,
    (Super_Bowl_flag + Labour_Day_flag + Thanksgiving_flag + Christmas_flag) AS total_holidays
FROM base_data
ORDER BY store, date;
