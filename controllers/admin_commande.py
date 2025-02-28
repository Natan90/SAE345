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


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()

    sql = '''
        SELECT C.id_commande, C.date_achat, U.login, 
               COUNT(LC.id_equipement) AS nbr_equipements,
               SUM(LC.prix * LC.quantite) AS prix_total,
               E.libelle_etat AS etat
        FROM COMMANDE C
        JOIN UTILISATEUR U ON C.id_utilisateur = U.id_utilisateur
        JOIN LIGNE_COMMANDE LC ON C.id_commande = LC.id_commande
        JOIN ETAT E ON C.id_etat = E.id_etat
        GROUP BY C.id_commande
        ORDER BY C.date_achat DESC;
    '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    id_commande = request.args.get('id_commande')
    equipements_commande = []

    if id_commande:
        sql = '''
            SELECT EQ.nom_equipement AS nom, LC.quantite, LC.prix, 
                   (LC.prix * LC.quantite) AS prix_ligne,
                   C.id_etat AS etat_id, LC.id_commande AS id
            FROM LIGNE_COMMANDE LC
            JOIN EQUIPEMENT_SPORT EQ ON LC.id_equipement = EQ.id_equipement
            JOIN COMMANDE C ON LC.id_commande = C.id_commande
            WHERE LC.id_commande = %s
        '''
        mycursor.execute(sql, (id_commande,))
        equipements_commande = mycursor.fetchall()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           equipements_commande=equipements_commande)



@admin_commande.route('/admin/commande/valider', methods=['POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()

    commande_id = request.form.get('id_commande')

    if commande_id:
        print("Commande à valider:", commande_id)
        sql = "UPDATE COMMANDE SET id_etat = 3 WHERE id_commande = %s"
        mycursor.execute(sql, (commande_id,))

        get_db().commit()

        return redirect('/admin/commande/show')

    return "Erreur : commande non trouvée", 400