#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db
#r
client_commande = Blueprint('client_commande', __name__, template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' selection des equipement_sport d'un panier '''
    equipement_sport_panier = []
    if len(equipement_sport_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html',
                           equipement_sport_panier=equipement_sport_panier,
                           prix_total=prix_total,
                           validation=1
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    sql = "SELECT * FROM LIGNE_PANIER WHERE id_utilisateur = %s"
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    sql = "INSERT INTO COMMANDE (date_achat, id_utilisateur, id_etat) VALUES (%s, %s, 1)"
    mycursor.execute(sql, (datetime.now(), id_client))
    id_commande = mycursor.lastrowid

    for item in items_ligne_panier:
        sql = "INSERT INTO LIGNE_COMMANDE (id_commande, id_equipement, prix, quantite) VALUES (%s, %s, (SELECT prix_equipement FROM EQUIPEMENT_SPORT WHERE id_equipement = %s), %s)"
        mycursor.execute(sql, (id_commande, item['id_equipement'], item['id_equipement'], item['quantite']))

    sql = "DELETE FROM LIGNE_PANIER WHERE id_utilisateur = %s"
    mycursor.execute(sql, (id_client,))
    get_db().commit()

    sql = '''
            SELECT
                COMMANDE.id_commande,
                COMMANDE.date_achat,
                SUM(LIGNE_COMMANDE.quantite) AS nbr_equipement_sport,
                SUM(LIGNE_COMMANDE.prix * LIGNE_COMMANDE.quantite) AS prix_total,
                ETAT.libelle_etat AS libelle
            FROM
                COMMANDE
            INNER JOIN
                LIGNE_COMMANDE ON COMMANDE.id_commande = LIGNE_COMMANDE.id_commande
            INNER JOIN
                ETAT ON COMMANDE.id_etat = ETAT.id_etat
            WHERE
                COMMANDE.id_commande = %s
            GROUP BY
                COMMANDE.id_commande
            '''

    mycursor.execute(sql, (id_commande,))
    nouvelle_commande = mycursor.fetchone()

    commandes = [nouvelle_commande]

    flash('commande ajoutée avec succès.', 'alert-success')
    return redirect('/client/equipement/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    sql='''SELECT
    COMMANDE.id_commande,
    SUM(LIGNE_COMMANDE.quantite) AS total_equipements
    FROM
    COMMANDE
    INNER JOIN
    LIGNE_COMMANDE ON COMMANDE.id_commande = LIGNE_COMMANDE.id_commande
    GROUP BY
    COMMANDE.id_commande;'''

    mycursor.execute(sql)
    nbr_equipements = mycursor.fetchall()


    sql = '''
        SELECT 
            COMMANDE.id_commande, 
            COMMANDE.date_achat, 
            SUM(LIGNE_COMMANDE.quantite) AS nbr_equipement_sport, 
            SUM(LIGNE_COMMANDE.prix * LIGNE_COMMANDE.quantite) AS prix_total, 
            ETAT.libelle_etat AS libelle
        FROM 
            COMMANDE
        INNER JOIN 
            LIGNE_COMMANDE ON COMMANDE.id_commande = LIGNE_COMMANDE.id_commande
        INNER JOIN 
            ETAT ON COMMANDE.id_etat = ETAT.id_etat
        WHERE 
            COMMANDE.id_utilisateur = %s
        GROUP BY 
            COMMANDE.id_commande
        '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    equipement_sport_commande = None
    commande_adresses = None

    id_commande = request.args.get('id_commande', None)

    if id_commande:
        print(str(id_commande) + "id_commande")
        sql = '''SELECT EQUIPEMENT_SPORT.nom_equipement AS nom, LIGNE_COMMANDE.quantite, LIGNE_COMMANDE.prix, (LIGNE_COMMANDE.quantite * LIGNE_COMMANDE.prix) AS prix_ligne
                FROM LIGNE_COMMANDE
                INNER JOIN EQUIPEMENT_SPORT ON LIGNE_COMMANDE.id_equipement = EQUIPEMENT_SPORT.id_equipement
                WHERE LIGNE_COMMANDE.id_commande = %s'''

        mycursor.execute(sql, (id_commande,))
        equipement_sport_commande = mycursor.fetchall()

        commande_adresses = []
        print(nbr_equipements)

    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           equipement_sport_commande=equipement_sport_commande,
                           commande_adresses=commande_adresses,
                           nbr_equipements=nbr_equipements
                           )

