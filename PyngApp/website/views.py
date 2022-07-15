#stored is the information regarding pages (views) a user can navigate to
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db, textPyng, inputEncoder, finalEncoder
import json
import pandas as pd


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST']) #called a decorator
@login_required
def home(): #whenever we go to slash, it will go to home function
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Write a longer note', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category = 'success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/textPyng', methods=['GET','POST'])
def predict():
    #features: island	bill_length_mm	bill_depth_mm	flipper_length_mm	body_mass_g	sex	year
    final_result = ""
    if request.method == 'POST':
        island = request.form['island']
        bill_length_mm = float(request.form['bill_length_mm'])
        bill_depth_mm = float(request.form['bill_depth_mm'])
        flipper_length_mm = float(request.form['flipper_length_mm'])
        body_mass_g = float(request.form['body_mass_g'])
        sex = (request.form['sex'])
        year = float(request.form['year'])

        input = [[island,bill_length_mm,
                                    bill_depth_mm,
                                    flipper_length_mm,
                                    body_mass_g,
                                    sex,
                                    year]]


        input_df = pd.DataFrame(input, columns=['island','bill_length_mm',
                                       'bill_depth_mm','flipper_length_mm',
                                       'body_mass_g','sex','year'])
        sc_train_X = input_df
        sc_train_X[['bill_length_mm',
            'bill_depth_mm',
            'flipper_length_mm',
            'body_mass_g']] = inputEncoder.transform(sc_train_X[['bill_length_mm',
                                      'bill_depth_mm',
                                      'flipper_length_mm',
                                      'body_mass_g']])

        train_X = finalEncoder.transform(sc_train_X)
        result = textPyng.predict(train_X)
        print("Hello!")
        print(result)
        if result:
            final_result = 'Model prediction done successfully! Result: ' + result
            flash(final_result, category = 'success')


    
    return render_template('textPyng.html', user=current_user)
