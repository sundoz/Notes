from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = 'super super super super super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = LoginManager()
manager.init_app(app)


oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='646440580568-cnb4voqsp8mr2o7aam6p13lvsokq8\
    mlm.apps.googleusercontent.com',
    client_secret='omZfQ1HqO5Vx86F34LUZx6i-',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'})
from pac import routes, models  # noqa
