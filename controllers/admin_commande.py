#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

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
    sql = '''SELECT UTILISATEUR.login, COMMANDE.date_achat, COUNT(LIGNE_COMMANDE.id_equipement) AS Nombre_equipements, 
                        COUNT(LIGNE_COMMANDE.prix) AS prix_total, COMMANDE.id_etat
             FROM COMMANDE
             JOIN UTILISATEUR ON COMMANDE.id_utilisateur = UTILISATEUR.id_utilisateur
             JOIN LIGNE_COMMANDE ON COMMANDE.id_commande = LIGNE_COMMANDE.id_commande
             JOIN EQUIPEMENT_SPORT ON LIGNE_COMMANDE.id_equipement = EQUIPEMENT_SPORT.id_equipement
             WHERE UTILISATEUR.id_utilisateur = %s
             GROUP BY UTILISATEUR.login, COMMANDE.date_achat, LIGNE_COMMANDE.prix, COMMANDE.id_etat
             ORDER BY COMMANDE.date_achat DESC'''
    mycursor.execute(sql, (admin_id,))
    commandes = mycursor.fetchall()

    commandes=[]

    equipements_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''  SELECT * FROM COMMANDE WHERE   '''
        commande_adresses = []
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , equipements_commande=equipements_commande
                           , commande_adresses=commande_adresses
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
