WITH city_count AS (
    SELECT local_id, count(*) AS db_count FROM Wikiaves_Photos GROUP BY local_id
)
UPDATE Locals_BR
SET db_count = city_count.db_count 
FROM city_count
WHERE Locals_BR.local_id = city_count.local_id;