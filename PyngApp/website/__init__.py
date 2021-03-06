from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pickle
from joblib import load
import tensorflow
from tensorflow.keras.models import model_from_json
 
db = SQLAlchemy()
DB_NAME = "database.db"

#Loading the text-based model
textPyng = pickle.load(open('pyngit.sav', 'rb'))

#Loading text-based model encoders
inputEncoder = load('scale_encoder.joblib') # load and reuse the model
finalEncoder = load('oneHot_encoder.joblib') # load and reuse the model

#Loading image-based model
# load json and create model
json_file = open('pyngresnet.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
imagePyng = model_from_json(loaded_model_json)

# load weights into new model
imagePyng.load_weights("pyngresnet.h5")

#loading dict_resnet for image model
with open('dict_resnet.pkl', 'rb') as f:
    dict_resnet = pickle.load(f)

def create_app():
    app = Flask(__name__) ##__name__ -> name of the file that was ran
    app.config['SECRET_KEY'] = 'chelsea football club'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #initialize database with app

    #register our views in our application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view =  'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

def create_database(application):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=application)
        print('Created Database.')