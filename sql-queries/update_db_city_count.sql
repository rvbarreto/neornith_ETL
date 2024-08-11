UPDATE Locals_BR SET
db_count = (
    SELECT COUNT(*) FROM Wikiaves_Photos WHERE local_id = {local_id}
    )
WHERE local_id = {local_id};