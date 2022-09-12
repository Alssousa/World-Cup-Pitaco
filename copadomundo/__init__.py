from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C0P4_D0_MUND0_P1T4C0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///worldcuppitaco.db'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from copadomundo import routes