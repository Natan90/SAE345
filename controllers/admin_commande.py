#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session
from datetime import datetime


from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()

    admin_id = session['id_user']
    sql = '''SELECT * FROM LIGNE_PANIER WHERE LIGNE_PANIER.id_utilisateur = %s'''
    mycursor.execute(sql, admin_id)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash('Votre panier est vide',)
        return redirect('/client/panier/show')

    date_commande= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, admin_id, "1")
    sql = '''INSERT INTO COMMANDE (date_achat, id_utilisateur, id_etat) VALUES (%s, %s, %s)'''
    mycursor.execute(sql, tuple_insert)
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)
    print(items_ligne_panier)
    print(admin_id)
    print(commande_id['last_insert_id'])
    print(commande_id)

    for item in items_ligne_panier:
        sql = "DELETE FROM LIGNE_PANIER WHERE id_utilisateur = %s AND id_equipement =%s"
        mycursor.execute(sql, admin_id, item['equipement_id'])
        sql = "SELECT prix FROM EQUIPEMENT_SPORT WHERE id_equipement = %s"
        mycursor.execute(sql, item['id_equipement'])
        prix = mycursor.fetchone()
        print(prix)
        sql = "INSERT INTO LIGNE_COMMANDE (id_commande, id_equipement, prix, quantite) VALUES (%s, %s, %s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['equipement_id'], prix['prix'], item['quantite'])
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        id_client = session['id_user']
        equipements_commande = None
        commande_adresses = None
        id_commande = request.args.get('id_commande', None)
        print(id_commande)
        if id_commande != None:
            sql = ''' '''
            commande_adresses = []
        return render_template('admin/commandes/show.html'
                               , equipements_commande=equipements_commande
                               , commande_adresses=commande_adresses
                               , id_commande=id_commande
                               , id_client=id_client

                               )






@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''           '''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
