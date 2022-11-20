from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C0P4_D0_MUND0_P1T4C0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://worldcuppitaco:Copadomundo2022@worldcuppitaco-db.mysql.database.azure.com:3306/worldcuppitaco?ssl_ca=DigiCertGlobalRootCA.crt.pem'
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#gerenciamento de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "É necessário fazer login antes para continuar."
login_manager.login_message_category = "alert-warning"

from copadomundo import routes