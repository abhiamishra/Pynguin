#stored is the information regarding pages (views) a user can navigate to
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean=True)


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"
    
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('pass1')
        password2 = request.form.get('pass2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters', category = 'error')
        elif password != password2:
            flash('Passwords must match', category = 'error')
        elif len(password) < 7:
            flash('Password must be atleast than 7 characters', category = 'error')
        else:
            flash("Account created!", category="userCreate")
            #add user to database
            pass
    return render_template("signup.html", text="Testing")
    #we can pass in values straight to the templates