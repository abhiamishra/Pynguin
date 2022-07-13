#stored is the information regarding pages (views) a user can navigate to
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db #from package, import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #querying database
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember=True) #Remembers the fact that user is logged in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category = 'error')
        else:
            flash('Email does not exist', category = 'error')


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required #makes sure that we can't logout unless we are logged in
def logout():
    logout_user() #logs out current user
    return redirect(url_for('auth.login'))
    
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('pass1')
        password2 = request.form.get('pass2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters', category = 'error')
        elif password != password2:
            flash('Passwords must match', category = 'error')
        elif len(password) < 7:
            flash('Password must be atleast than 7 characters', category = 'error')
        else:
            new_user = User(email=email, first_name = firstName, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) #Remembers the fact that user is logged in
            flash("Account created!", category="success")
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
    #we can pass in values straight to the templates