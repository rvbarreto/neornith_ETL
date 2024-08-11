INSERT INTO Locals_BR (local_id, city, state_name, state_acronym, db_count, db_wikiaves) 
    VALUES (
        {local_id},
        {city},
        {state_name},
        {state_acronym},
        0,
        0
        ) ON CONFLICT DO NOTHING;