#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/equipement/commentaires', methods=['GET'])
def admin_equipement_details():
    mycursor = get_db().cursor()
    id_equipement =  request.args.get('id_equipement', None)
    sql = '''    requête admin_type_equipement_1    '''
    commentaires = {}
    sql = '''   requête admin_type_equipement_1_bis   '''
    equipement = []
    sql = '''   requête admin_type_equipement_1_3   '''
    nb_commentaires = []
    return render_template('admin/equipement/show_equipement_commentaires.html'
                           , commentaires=commentaires
                           , equipement=equipement
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/equipement/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_equipement = request.form.get('id_equipement', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''    requête admin_type_equipement_2   '''
    tuple_delete=(id_utilisateur,id_equipement,date_publication)
    get_db().commit()
    return redirect('/admin/equipement/commentaires?id_equipement='+id_equipement)


@admin_commentaire.route('/admin/equipement/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_equipement = request.args.get('id_equipement', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/equipement/add_commentaire.html',id_utilisateur=id_utilisateur,id_equipement=id_equipement,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_equipement = request.form.get('id_equipement', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    requête admin_type_equipement_3   '''
    get_db().commit()
    return redirect('/admin/equipement/commentaires?id_equipement='+id_equipement)


@admin_commentaire.route('/admin/equipement/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_equipement = request.args.get('id_equipement', None)
    mycursor = get_db().cursor()
    sql = '''   requête admin_type_equipement_4   '''
    get_db().commit()
    return redirect('/admin/equipement/commentaires?id_equipement='+id_equipement)