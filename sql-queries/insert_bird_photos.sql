INSERT INTO Bird_Species (binomial_name, pt_br) VALUES ({sp_cientifico}, {sp_popular}) ON CONFLICT DO NOTHING;
INSERT INTO Wikiaves_Photos (
        reg_id,
        binomial_name,
        sp_id,
        sp_wiki,
        autor,
        autor_perfil,
        reg_date,
        questionado,
        local_id,
        coms,
        likes,
        vis
    ) VALUES (
        {reg_id},
        {sp_cientifico},
        {sp_id},
        {sp_wiki},
        {reg_autor},
        {autor_perfil},
        TO_DATE({reg_data}, 'DD/MM/YYYY'),
        {reg_questionado},
        {local_id},
        {reg_coms},
        {reg_likes},
        {reg_vis}
    ) ON CONFLICT DO NOTHING;