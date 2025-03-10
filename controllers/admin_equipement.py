#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_equipement = Blueprint('admin_equipement', __name__,
                          template_folder='templates')


@admin_equipement.route('/admin/equipement/show')
def show_equipement():
    mycursor = get_db().cursor()
    sql = '''  select * from EQUIPEMENT_SPORT
    '''
    mycursor.execute(sql)
    equipements = mycursor.fetchall()
    print(equipements)
    return render_template('admin/equipement/show_equipement.html', equipements=equipements)


@admin_equipement.route('/admin/equipement/add', methods=['GET'])
def add_equipement():
    mycursor = get_db().cursor()
    sql=''' SELECT * FROM TYPE_EQUIPEMENT_SPORT'''
    mycursor.execute(sql)
    type_equipement = mycursor.fetchall()
    return render_template('admin/equipement/add_equipement.html'
                           ,types_equipement=type_equipement,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_equipement.route('/admin/equipement/add', methods=['POST'])
def valid_add_equipement():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_equipement_id = request.form.get('type_equipement_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  INSERT INTO 
    EQUIPEMENT_SPORT (id_equipement,nom_equipement,image,prix_equipement,id_type_equipement_sport,description,id_taille,id_couleur) 
    VALUES (NULL,%s,%s,%s,%s,%s,1,1) '''

    tuple_add = (nom, filename, prix, type_equipement_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'equipement ajouté , nom: ', nom, ' - type_equipement:', type_equipement_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'equipement ajouté , nom:' + nom + '- type_equipement:' + type_equipement_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/equipement/show')


@admin_equipement.route('/admin/equipement/delete', methods=['GET'])
def delete_equipement():
    id_equipement=request.args.get('id_equipement')
    mycursor = get_db().cursor()
    """
    sql = ''' requête admin_equipement_3 '''
    mycursor.execute(sql, id_equipement)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet equipement : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    
    else:
    """
    sql = ''' SELECT COUNT(id_commande) as nbr_dep FROM LIGNE_COMMANDE WHERE id_equipement = %s'''
    mycursor.execute(sql, id_equipement)
    nombre_dependences_commandes = mycursor.fetchone()
    print(nombre_dependences_commandes['nbr_dep']," <- RESULTS")
    if  nombre_dependences_commandes['nbr_dep'] > 0:
        flash("Il y a {} dépendence(s)".format(nombre_dependences_commandes['nbr_dep']))
        return redirect("/admin/equipement/show")
    sql = ''' SELECT image FROM EQUIPEMENT_SPORT WHERE id_equipement = %s'''
    mycursor.execute(sql, id_equipement)
    equipement = mycursor.fetchone()
    print(equipement)

    image = equipement['image']
    sql = ''' DELETE FROM EQUIPEMENT_SPORT WHERE id_equipement=%s '''
    mycursor.execute(sql, id_equipement)
    get_db().commit()


    #if image != None:
        #os.remove('static/images/' + image) # évite de supprimer l'image pour l'instant

    print("un equipement supprimé, id :", id_equipement)
    message = u'un equipement supprimé, id : ' + id_equipement
    flash(message, 'alert-success')

    return redirect('/admin/equipement/show')


@admin_equipement.route('/admin/equipement/edit', methods=['GET'])
def edit_equipement():
    id_equipement=request.args.get('id_equipement')
    mycursor = get_db().cursor()
    sql = '''
    select * from EQUIPEMENT_SPORT where id_equipement = %s 
    '''
    mycursor.execute(sql, id_equipement)
    equipement = mycursor.fetchone()
    print(equipement)
    sql = '''
    select * from TYPE_EQUIPEMENT_SPORT
    '''
    mycursor.execute(sql)
    types_equipement = mycursor.fetchall()

    # sql = '''
    # requête admin_equipement_6
    # '''
    # mycursor.execute(sql, id_equipement)
    # declinaisons_equipement = mycursor.fetchall()

    return render_template('admin/equipement/edit_equipement.html'
                           ,equipement=equipement
                           ,types_equipement=types_equipement
                           #,declinaisons_equipement=declinaisons_equipement
                           )


@admin_equipement.route('/admin/equipement/edit', methods=['POST'])
def valid_edit_equipement():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_equipement = request.form.get('id_equipement')
    image = request.files.get('image', '')
    type_equipement_id = request.form.get('type_equipement_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')
    sql = '''
        select image from EQUIPEMENT_SPORT where id_equipement = %s 
       '''
    mycursor.execute(sql, id_equipement)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        #if image_nom != "" and image_nom is not None and os.path.exists(
                #os.path.join(os.getcwd() + "/static/images/", image_nom)):
                #os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''          
       UPDATE EQUIPEMENT_SPORT 
       SET nom_equipement=%s,image=%s,prix_equipement=%s,id_type_equipement_sport=%s,description=%s
       WHERE id_equipement=%s  '''
    mycursor.execute(sql, (nom, image_nom, prix, type_equipement_id, description, id_equipement))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'equipement modifié , nom:' + nom + '- type_equipement :' + type_equipement_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/equipement/show')







@admin_equipement.route('/admin/equipement/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    equipement=[]
    commentaires = {}
    return render_template('admin/equipement/show_avis.html'
                           , equipement=equipement
                           , commentaires=commentaires
                           )


@admin_equipement.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    equipement_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(equipement_id)
