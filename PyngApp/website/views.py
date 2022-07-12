#stored is the information regarding pages (views) a user can navigate to
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #called a decorator
def home(): #whenever we go to slash, it will go to home function
    return render_template("home.html")

