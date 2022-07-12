from flask import Flask

def create_app():
    app = Flask(__name__) ##__name__ -> name of the file that was ran
    app.config['SECRET_KEY'] = 'chelsea football club'

    #register our views in our application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app