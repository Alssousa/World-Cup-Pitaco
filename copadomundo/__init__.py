from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import urllib.parse

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=worldcuppitaco-db.mysql.database.azure.com;DATABASE=worldcuppitaco;UID=worldcuppitaco;PWD=Copadomundo2022")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C0P4_D0_MUND0_P1T4C0'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#gerenciamento de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "É necessário fazer login antes para continuar."
login_manager.login_message_category = "alert-warning"

from copadomundo import routes