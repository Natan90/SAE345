#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_equipement = Blueprint('client_equipement', __name__,
                        template_folder='templates')


@client_equipement.route('/client/equipement/show')
def client_equipement_show():
    mycursor = get_db().cursor()

    query = "SELECT * FROM EQUIPEMENT_SPORT WHERE 1=1"
    params = []

    if 'filter_word' in session and session['filter_word']:
        query += " AND nom_equipement LIKE %s"
        params.append("%{}%".format(session['filter_word']))

    if 'filter_prix_min' in session and session['filter_prix_min']:
        query += " AND prix_equipement >= %s"
        params.append(session['filter_prix_min'])

    if 'filter_prix_max' in session and session['filter_prix_max']:
        query += " AND prix_equipement <= %s"
        params.append(session['filter_prix_max'])

    if 'filter_types' in session and session['filter_types']:
        type_placeholders = ', '.join(['%s'] * len(session['filter_types']))
        if type_placeholders:
            query += " AND type_equipement_id IN ({})".format(type_placeholders)
            params.extend(session['filter_types'])

    if 'filter_taille' in session and session['filter_taille']:
        query += " AND taille_id = %s"
        params.append(session['filter_taille'])

    mycursor.execute(query, params)
    equipements = mycursor.fetchall()

    mycursor.execute("SELECT * FROM TYPE_EQUIPEMENT_SPORT")
    types_equipement = mycursor.fetchall()

    id_client = session['id_user']

    sql = "SELECT EQUIPEMENT_SPORT.nom_equipement AS nom, EQUIPEMENT_SPORT.prix_equipement AS prix, LIGNE_PANIER.quantite, EQUIPEMENT_SPORT.id_equipement, COALESCE(EQUIPEMENT_SPORT.stock, 0) AS stock FROM LIGNE_PANIER JOIN EQUIPEMENT_SPORT ON LIGNE_PANIER.id_equipement = EQUIPEMENT_SPORT.id_equipement WHERE LIGNE_PANIER.id_utilisateur = %s"


    mycursor.execute(sql, (id_client,))
    equipements_panier = mycursor.fetchall()
    for equipement in equipements_panier:
        equipement['stock'] = equipement['stock'] if equipement['stock'] is not None else 0

    prix_total = sum(item['quantite'] * item['prix'] for item in equipements_panier)

    return render_template('client/boutique/panier_equipement.html',
                           equipements=equipements,
                           equipements_panier=equipements_panier,
                           items_filtre=types_equipement,
                           prix_total=prix_total)


