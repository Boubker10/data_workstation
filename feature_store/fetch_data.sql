-- fetch_data.sql
-- Récupère les données brutes walmart pour un portefeuille de stores et une plage de dates

-- Paramètres à remplacer selon besoin : 
-- - :store_list (array d'entiers)
-- - :start_date (date)
-- - :end_date (date)

SELECT *
FROM walmart
WHERE Store = ANY(:store_list)
  AND Date BETWEEN :start_date AND :end_date
ORDER BY Store, Date;
