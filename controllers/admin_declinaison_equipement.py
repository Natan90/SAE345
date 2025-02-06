#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_equipement = Blueprint('admin_declinaison_equipement', __name__,
                         template_folder='templates')


@admin_declinaison_equipement.route('/admin/declinaison_equipement/add')
def add_declinaison_equipement():
    id_equipement=request.args.get('id_equipement')
    mycursor = get_db().cursor()
    equipement=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/equipement/add_declinaison_equipement.html'
                           , equipement=equipement
                           , couleurs=couleurs
                           , tailles=tailles
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_equipement.route('/admin/declinaison_equipement/add', methods=['POST'])
def valid_add_declinaison_equipement():
    mycursor = get_db().cursor()

    id_equipement = request.form.get('id_equipement')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')
    # attention au doublon
    get_db().commit()
    return redirect('/admin/equipement/edit?id_equipement=' + id_equipement)


@admin_declinaison_equipement.route('/admin/declinaison_equipement/edit', methods=['GET'])
def edit_declinaison_equipement():
    id_declinaison_equipement = request.args.get('id_declinaison_equipement')
    mycursor = get_db().cursor()
    declinaison_equipement=[]
    couleurs=None
    tailles=None
    d_taille_uniq=None
    d_couleur_uniq=None
    return render_template('admin/equipement/edit_declinaison_equipement.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_equipement=declinaison_equipement
                           , d_taille_uniq=d_taille_uniq
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_equipement.route('/admin/declinaison_equipement/edit', methods=['POST'])
def valid_edit_declinaison_equipement():
    id_declinaison_equipement = request.form.get('id_declinaison_equipement','')
    id_equipement = request.form.get('id_equipement','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_equipement modifié , id:' + str(id_declinaison_equipement) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/equipement/edit?id_equipement=' + str(id_equipement))


@admin_declinaison_equipement.route('/admin/declinaison_equipement/delete', methods=['GET'])
def admin_delete_declinaison_equipement():
    id_declinaison_equipement = request.args.get('id_declinaison_equipement','')
    id_equipement = request.args.get('id_equipement','')

    flash(u'declinaison supprimée, id_declinaison_equipement : ' + str(id_declinaison_equipement),  'alert-success')
    return redirect('/admin/equipement/edit?id_equipement=' + str(id_equipement))
