#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session, url_for

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_equipement = request.form.get('id_equipement')
    quantite = request.form.get('quantite')

    sql = "SELECT * FROM LIGNE_PANIER WHERE id_equipement = %s AND id_utilisateur = %s"
    mycursor.execute(sql, (id_equipement, id_client))
    casque_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM EQUIPEMENT_SPORT WHERE id_equipement = %s", (id_equipement,))
    casque = mycursor.fetchone()

    if not (casque_panier is None) and casque_panier['quantite'] >= 1:
        turtle_update = (quantite, id_client, id_equipement)
        sql = "UPDATE LIGNE_PANIER SET quantite = quantite+%s WHERE id_utilisateur = %s AND id_equipement=%s"
        mycursor.execute(sql, turtle_update)

        sql_stock = "UPDATE EQUIPEMENT_SPORT SET stock = stock - %s WHERE id_equipement = %s"
        mycursor.execute(sql_stock, (quantite, id_equipement))
    else:
        tuple_insert = (id_client, id_equipement, quantite)
        sql = "INSERT INTO LIGNE_PANIER(id_utilisateur, id_equipement, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)"
        mycursor.execute(sql, tuple_insert)

        sql_stock = "UPDATE EQUIPEMENT_SPORT SET stock = stock - %s WHERE id_equipement = %s"
        mycursor.execute(sql_stock, (quantite, id_equipement))

        flash("Equipment added to cart.", "success")

    get_db().commit()

    return redirect('/client/equipement/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_equipement = request.form.get('id_equipement', '')
    quantite = 1

    sql = "SELECT * FROM LIGNE_PANIER WHERE id_equipement = %s AND id_utilisateur = %s"
    mycursor.execute(sql, (id_equipement, id_client))
    equipement_panier = mycursor.fetchone()

    if not(equipement_panier is None) and equipement_panier['quantite'] > 1:
        sql_upd = "UPDATE LIGNE_PANIER SET quantite = quantite - %s WHERE id_utilisateur = %s AND id_equipement = %s"
        mycursor.execute(sql_upd, (quantite, id_client, id_equipement))

        sql_stock = "UPDATE EQUIPEMENT_SPORT SET stock = stock + %s WHERE id_equipement = %s"
        mycursor.execute(sql_stock, (quantite, id_equipement))
    else:
        sql_del = "DELETE FROM LIGNE_PANIER WHERE id_utilisateur = %s AND id_equipement = %s"
        mycursor.execute(sql_del, (id_client, id_equipement))

        sql_stock = "UPDATE EQUIPEMENT_SPORT SET stock = stock + %s WHERE id_equipement = %s"
        mycursor.execute(sql_stock, (quantite, id_equipement))

    get_db().commit()
    return redirect('/client/equipement/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql_select_panier = "SELECT * FROM LIGNE_PANIER WHERE id_utilisateur = %s"
    mycursor.execute(sql_select_panier, (client_id,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        sql = "DELETE FROM LIGNE_PANIER WHERE id_utilisateur = %s AND id_equipement = %s"
        mycursor.execute(sql, (client_id, item['id_equipement']))

        sql = "UPDATE EQUIPEMENT_SPORT SET stock = stock + %s WHERE id_equipement = %s"
        mycursor.execute(sql, (item['quantite'], item['id_equipement']))
        get_db().commit()
    return redirect('/client/equipement/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_casque = request.form.get('id_casque')
    # id_declinaison_casque = request.form.get('id_declinaison_casque')

    sql_quantite = "SELECT quantite FROM LIGNE_PANIER WHERE utilisateur_id = %s AND casque_id = %s"
    mycursor.execute(sql_quantite, (id_client, id_casque))
    quantite = mycursor.fetchone()

    sql_delete_line = "DELETE FROM LIGNE_PANIER WHERE utilisateur_id = %s AND casque_id = %s"
    mycursor.execute(sql_delete_line, (id_client, id_casque))

    sql_update_stock = "UPDATE EQUIPEMENT_SPORT SET stock = stock + %s WHERE id_casque = %s"
    mycursor.execute(sql_update_stock, (quantite['quantite'], id_casque))


    get_db().commit()
    return redirect('/client/casque/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    session['filter_word'] = request.form.get('filter_word', '').strip()
    session['filter_prix_min'] = request.form.get('filter_prix_min', '').strip()
    session['filter_prix_max'] = request.form.get('filter_prix_max', '').strip()
    session['filter_types'] = request.form.getlist('filter_types')
    session['filter_taille'] = request.form.get('filter_taille', '').strip()

    return redirect('/client/casque/show')





@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def supprimer_filtre():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    session.pop('filter_taille', None)


    return redirect('/client/casque/show')

