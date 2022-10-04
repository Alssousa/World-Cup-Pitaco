from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C0P4_D0_MUND0_P1T4C0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worldcuppitaco.db'
app.config['SESSION_PERMANET'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#gerenciamento de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "É necessário fazer login antes para continuar."
login_manager.login_message_category = "alert-warning"

from copadomundo import routes