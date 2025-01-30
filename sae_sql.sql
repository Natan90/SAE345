DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS LIGNE;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS EQUIPEMENT_SPORT;
DROP TABLE IF EXISTS TAILLE;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS TYPE_EQUIPEMENT_SPORT;
DROP TABLE IF EXISTS COULEUR;

CREATE TABLE COULEUR (
    id_couleur INT AUTO_INCREMENT,
    nom_couleur VARCHAR(50),
    PRIMARY KEY(id_couleur)
);

CREATE TABLE TYPE_EQUIPEMENT_SPORT (
    id_type_equipement_sport INT AUTO_INCREMENT,
    libelle_type_equipement_sport VARCHAR(50),
    PRIMARY KEY(id_type_equipement_sport)
);

CREATE TABLE UTILISATEUR (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(50),
    email VARCHAR(50),
    nom VARCHAR(50),
    role VARCHAR(50),
    password VARCHAR(255),
    est_actif BOOLEAN,
    PRIMARY KEY(id_utilisateur)
);

CREATE TABLE ETAT (
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(50),
    PRIMARY KEY(id_etat)
);

CREATE TABLE TAILLE (
    id_taille INT AUTO_INCREMENT,
    libelle_taille VARCHAR(50),
    PRIMARY KEY(id_taille)
);

CREATE TABLE EQUIPEMENT_SPORT (
    id_equipement INT AUTO_INCREMENT,
    nom_equipement VARCHAR(50),
    prix_equipement DECIMAL(15,2),
    matiere VARCHAR(50),
    description VARCHAR(50),
    fournisseur VARCHAR(50),
    marque VARCHAR(50),
    poids DECIMAL(15,2),
    d_occasion BOOLEAN,
    image VARCHAR(50),
    id_taille INT NOT NULL,
    id_type_equipement_sport INT NOT NULL,
    id_couleur INT NOT NULL,
    PRIMARY KEY(id_equipement),
    FOREIGN KEY(id_taille) REFERENCES TAILLE(id_taille),
    FOREIGN KEY(id_type_equipement_sport) REFERENCES TYPE_EQUIPEMENT_SPORT(id_type_equipement_sport),
    FOREIGN KEY(id_couleur) REFERENCES COULEUR(id_couleur)
);

CREATE TABLE COMMANDE (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    id_utilisateur INT NOT NULL,
    id_etat INT NOT NULL,
    PRIMARY KEY(id_commande),
    FOREIGN KEY(id_etat) REFERENCES ETAT(id_etat),
    FOREIGN KEY(id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur)
);

CREATE TABLE ligne_commande (
    id_equipement INT,
    id_commande INT,
    prix DECIMAL(15,2),
    quantite INT,
    PRIMARY KEY(id_equipement, id_commande),
    FOREIGN KEY(id_equipement) REFERENCES EQUIPEMENT_SPORT(id_equipement),
    FOREIGN KEY(id_commande) REFERENCES COMMANDE(id_commande)
);

CREATE TABLE ligne_panier (
    id_equipement INT,
    id_utilisateur INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY(id_equipement, id_utilisateur),
    FOREIGN KEY(id_equipement) REFERENCES EQUIPEMENT_SPORT(id_equipement),
    FOREIGN KEY(id_utilisateur) REFERENCES UTILISATEUR(id_utilisateur)
);

INSERT INTO COULEUR (id_couleur, nom_couleur) VALUES
    (1, 'Rouge'),
    (2, 'Bleu'),
    (3, 'Vert'),
    (4, 'Jaune'),
    (5, 'Noir');

INSERT INTO TYPE_EQUIPEMENT_SPORT (id_type_equipement_sport, libelle_type_equipement_sport) VALUES
    (1, 'Ballon'),
    (2, 'Raquette'),
    (3, 'Vélo'),
    (4, 'Gant'),
    (5, 'Filet');

INSERT INTO UTILISATEUR (id_utilisateur, login, password, role, est_actif, nom, email) VALUES
    (1, 'admin', 'pbkdf2:sha256:600000$VQJnbWSkoyzKReNL$c510c74149e9eea7d47fd1242064dd8bcc2968555f41c107ba0da395ab160de2', 'ROLE_admin', 1, 'admin', 'admin@admin.fr'),
    (2, 'client', 'pbkdf2:sha256:600000$ABCsJQjDITt5Fx0k$8997971258697acd2c995ed1d5d3fb7806110e4effe562866930134273dd56b2', 'ROLE_client', 1, 'client', 'client@client.fr'),
    (3, 'client2', 'pbkdf2:sha256:600000$Cba5KP6zIM04OMWA$e7fe8b4513ff81bf761464d12d95e1d5cbafec2dfba932ffb9de74faa6bd3eb0', 'ROLE_client', 1, 'client2', 'client2@client2.fr');

INSERT INTO ETAT (id_etat, libelle_etat) VALUES
    (1, 'En attente'),
    (2, 'Confirmée'),
    (3, 'Expédiée'),
    (4, 'Livrée'),
    (5, 'Annulée');

INSERT INTO TAILLE (id_taille, libelle_taille) VALUES
    (1, 'Petit'),
    (2, 'Moyen'),
    (3, 'Grand'),
    (4, 'Très Grand'),
    (5, 'Très Très Grand');

INSERT INTO EQUIPEMENT_SPORT (id_equipement, nom_equipement, prix_equipement, matiere, description, fournisseur, marque, poids, d_occasion, id_taille, id_type_equipement_sport, id_couleur, image) VALUES
    (1, 'Altère 15kg', 50.00, 'Acier', 'Altère de 15kg pour musculation', 'Decathlon', 'Domyos', 15.0, 0, 1, 1, 5, 'Altere_15Kg.png'),
    (2, 'Altère 30kg', 90.00, 'Acier', 'Altère de 30kg pour musculation', 'Decathlon', 'Domyos', 30.0, 0, 2, 1, 5, 'Altere_30Kg.png'),
    (3, 'Ballon Noir', 25.00, 'Cuir', 'Ballon de sport noir', 'Nike', 'Nike', 0.6, 0, 3, 2, 1, 'Ballon_noir.png'),
    (4, 'Ballon Rouge', 25.00, 'Cuir', 'Ballon de sport rouge', 'Nike', 'Nike', 0.6, 0, 3, 2, 4, 'Ballon_rouge.png'),
    (5, 'Gants de boxe Noirs', 40.00, 'Cuir', 'Gants de boxe noirs pour compétition', 'Everlast', 'Everlast', 0.4, 0, 3, 4, 5, 'Gants_Boxe_Noirs.png'),
    (6, 'Gants de boxe Rouges', 40.00, 'Cuir', 'Gants de boxe rouges pour compétition', 'Everlast', 'Everlast', 0.4, 0, 3, 4, 4, 'Gants_Boxe_Rouges.png'),
    (7, 'Masque de plongée Noir', 20.00, 'Silicone', 'Masque de plongée noir', 'Cressi', 'Cressi', 0.3, 0, 4, 3, 5, 'Masque_Plongee_Bleu.png'),
    (8, 'Masque de plongée Transparent', 20.00, 'Silicone', 'Masque de plongée transparent', 'Cressi', 'Cressi', 0.3, 0, 4, 3, 3, 'Masque_Plongee_Noir.png'),
    (9, 'Palmes Jaunes', 30.00, 'Plastique', 'Palmes jaunes pour natation', 'Arena', 'Arena', 0.5, 0, 4, 5, 4, 'Masque_Plongee_Transparent.png'),
    (10, 'Palmes Noires', 30.00, 'Plastique', 'Palmes noires pour natation', 'Arena', 'Arena', 0.5, 0, 4, 5, 5, 'Palmes_Jaunes.png'),
    (11, 'Palmes Vertes', 30.00, 'Plastique', 'Palmes vertes pour natation', 'Arena', 'Arena', 0.5, 0, 4, 5, 3, 'Palmes_Noirs.png'),
    (12, 'Patins Noirs', 60.00, 'Cuir', 'Patins noirs pour patinage', 'Rollerblade', 'Rollerblade', 1.2, 0, 3, 3, 5, 'Palmes_Vert.png'),
    (13, 'Piolet Bleu', 120.00, 'Métal', 'Piolet bleu pour alpinisme', 'Black Diamond', 'Black Diamond', 0.8, 0, 4, 4, 2, 'Patins_Noir.png'),
    (14, 'Piolet Jaune', 120.00, 'Métal', 'Piolet jaune pour alpinisme', 'Black Diamond', 'Black Diamond', 0.8, 0, 4, 4, 4, 'Piolet_Bleu.png'),
    (15, 'Piolet Noir', 120.00, 'Métal', 'Piolet noir pour alpinisme', 'Black Diamond', 'Black Diamond', 0.8, 0, 4, 4, 5, 'Piolet_Jaune.png'),
    (16, 'Piolet Rouge', 120.00, 'Métal', 'Piolet rouge pour alpinisme', 'Black Diamond', 'Black Diamond', 0.8, 0, 4, 4, 4, 'Piolet_Rouge.png'),
    (17, 'Raquette de ping-pong Bleue', 35.00, 'Bois', 'Raquette bleue pour ping-pong', 'Cornilleau', 'Cornilleau', 0.3, 0, 3, 2, 2, 'Raquette_PingPong_Bleue.png');

INSERT INTO COMMANDE (id_commande, date_achat, id_utilisateur, id_etat) VALUES
    (1, '2025-01-01', 1, 1),
    (2, '2025-01-02', 2, 1),
    (3, '2025-01-03', 1, 5),
    (4, '2025-01-04', 1, 5),
    (5, '2025-01-05', 1, 5);

INSERT INTO ligne_commande (id_equipement, id_commande, prix, quantite) VALUES
    (1, 1, 20.50, 1),
    (2, 2, 70.00, 2),
    (3, 3, 499.99, 1),
    (4, 4, 35.99, 4),
    (5, 5, 25.99, 3);

INSERT INTO ligne_panier (id_equipement, id_utilisateur, quantite, date_ajout) VALUES
    (1, 1, 1, '2025-01-10'),
    (2, 2, 2, '2025-01-11'),
    (3, 3, 1, '2025-01-12'),
    (4, 1, 3, '2025-01-13'),
    (5, 2, 2, '2025-01-14');