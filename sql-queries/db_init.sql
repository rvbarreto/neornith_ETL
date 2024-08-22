CREATE TABLE Bird_Species (
       binomial_name VARCHAR(64) PRIMARY KEY,
       pt_br VARCHAR(64) NULL,
       eng VARCHAR(64) NULL
);
CREATE TABLE Locals_BR (
       local_id INTEGER PRIMARY KEY,
       city VARCHAR(64) NOT NULL,
       state_name VARCHAR(32) NOT NULL,
       state_acronym VARCHAR(2) NOT NULL,
       db_count INTEGER NOT NULL,
       db_wikiaves INTEGER NOT NULL,
       last_update DATE NOT NULL DEFAULT CURRENT_DATE,
);
ALTER TABLE Locals_BR ADD last_update DATE NOT NULL DEFAULT CURRENT_DATE; 
CREATE TABLE Wikiaves_Photos (
       reg_id INTEGER PRIMARY KEY,
       binomial_name VARCHAR(64) NOT NULL,
       sp_id INTEGER NULL,
       sp_wiki VARCHAR(64) NOT NULL,
       autor VARCHAR(64) NOT NULL,
       autor_perfil VARCHAR(128) NOT NULL,
       reg_date DATE NOT NULL,
       questionado BOOLEAN NOT NULL,
       local_id INTEGER NOT NULL,
       coms INTEGER NOT NULL,
       likes INTEGER NOT NULL,
       vis INTEGER NOT NULL,
       FOREIGN KEY (binomial_name) REFERENCES Bird_Species(binomial_name),
       FOREIGN KEY (local_id) REFERENCES Locals_BR(local_id)
);
CREATE TABLE Wikiaves_Photo_Metadata (
       reg_id INTEGER PRIMARY KEY,
       brand VARCHAR(32) NULL,
       model VARCHAR(32) NULL,
       shutter_speed VARCHAR(8) NULL,
       aperture VARCHAR(8) NULL,
       iso VARCHAR(8) NULL,
       exif_date TIMESTAMP NULL,
       flash BOOLEAN NULL,
       focal_distance VARCHAR(32) NULL,
       mode VARCHAR(8) NULL,
       white_balance VARCHAR(16) NULL,
       capture_mode VARCHAR(32) NULL,
       FOREIGN KEY (reg_id) REFERENCES Wikiaves_Photos(reg_id)
);

COMMENT on column Wikiaves_Photo_Metadata.brand IS 'Fabricante';
COMMENT on column Wikiaves_Photo_Metadata.model IS 'Câmera';
COMMENT on column Wikiaves_Photo_Metadata.shutter_speed IS 'Tempo de Exposição';
COMMENT on column Wikiaves_Photo_Metadata.aperture IS 'Abertura';
COMMENT on column Wikiaves_Photo_Metadata.iso IS 'Velocidade ISO';
COMMENT on column Wikiaves_Photo_Metadata.exif_date IS 'Date e hora em que foi tirada';
COMMENT on column Wikiaves_Photo_Metadata.flash IS 'Flash';
COMMENT on column Wikiaves_Photo_Metadata.focal_distance IS 'Distância Focal';
COMMENT on column Wikiaves_Photo_Metadata.mode IS 'Modo de exposição';
COMMENT on column Wikiaves_Photo_Metadata.white_balance IS 'Equilíbrio de Branco';
COMMENT on column Wikiaves_Photo_Metadata.capture_mode IS 'Tipo de Captura de Cena';
