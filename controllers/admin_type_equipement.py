#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_equipement = Blueprint('admin_type_equipement', __name__,
                        template_folder='templates')

@admin_type_equipement.route('/admin/type-equipement/show')
def show_type_equipement():
    mycursor = get_db().cursor()
    sql = '''  SELECT TYPE_EQUIPEMENT_SPORT.id_type_equipement_sport,libelle_type_equipement_sport,COUNT(id_equipement) AS nbr_equipements
    FROM TYPE_EQUIPEMENT_SPORT 
    JOIN EQUIPEMENT_SPORT 
    ON EQUIPEMENT_SPORT.id_type_equipement_sport = TYPE_EQUIPEMENT_SPORT.id_type_equipement_sport 
    GROUP BY TYPE_EQUIPEMENT_SPORT.id_type_equipement_sport,libelle_type_equipement_sport'''
    mycursor.execute(sql)
    types_equipement = mycursor.fetchall()
    return render_template('admin/type_equipement/show_type_equipement.html', types_equipement=types_equipement)

@admin_type_equipement.route('/admin/type-equipement/add', methods=['GET'])
def add_type_equipement():
    return render_template('admin/type_equipement/add_type_equipement.html')

@admin_type_equipement.route('/admin/type-equipement/add', methods=['POST'])
def valid_add_type_equipement():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle)
    conn=get_db()
    mycursor = conn.cursor()
    sql = '''    INSERT INTO TYPE_EQUIPEMENT_SPORT VALUES (NULL,%s)   '''
    mycursor.execute(sql, tuple_insert)
    conn.commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-equipement/show') #url_for('show_type_equipement')

@admin_type_equipement.route('/admin/type-equipement/delete', methods=['GET'])
def delete_type_equipement():
    id_type_equipement = request.args.get('id_type_equipement', '')
    mycursor = get_db().cursor()
    sql="""   SELECT COUNT(id_equipement) as nbr_dep from EQUIPEMENT_SPORT where id_type_equipement_sport=%s"""
    mycursor.execute(sql, id_type_equipement)
    result=mycursor.fetchone()
    if result['nbr_dep']!=0:
        flash("Nombre de dépendences non null, il y a {} dépendences".format(result['nbr_dep']))
        return redirect("/admin/type-equipement/show")
    sql="""DELETE FROM TYPE_EQUIPEMENT_SPORT WHERE id_type_equipement_sport = %s"""
    mycursor.execute(sql, id_type_equipement)
    get_db().commit()

    flash(u'suppression type equipement , id : ' + id_type_equipement, 'alert-success')
    return redirect('/admin/type-equipement/show')

@admin_type_equipement.route('/admin/type-equipement/edit', methods=['GET'])
def edit_type_equipement():
    id_type_equipement = request.args.get('id_type_equipement', '')
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM TYPE_EQUIPEMENT_SPORT WHERE id_type_equipement_sport=%s  '''
    mycursor.execute(sql, (id_type_equipement))
    type_equipement = mycursor.fetchone()
    return render_template('admin/type_equipement/edit_type_equipement.html', type_equipement=type_equipement)

@admin_type_equipement.route('/admin/type-equipement/edit', methods=['POST'])
def valid_edit_type_equipement():
    libelle = request.form['libelle']
    id_type_equipement = request.form.get('id_type_equipement', '')
    tuple_update = (libelle, id_type_equipement)
    mycursor = get_db().cursor()
    sql = ''' UPDATE TYPE_EQUIPEMENT_SPORT SET libelle_type_equipement_sport = %s WHERE  id_type_equipement_sport = %s  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type equipement modifié, id: ' + id_type_equipement + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-equipement/show')








