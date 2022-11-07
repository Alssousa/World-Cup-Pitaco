from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
'''from sqlalchemy import create_engine
from urllib.parse import quote_plus

engine = create_engine("mysql+pymysql://%s:%s@worldcuppitaco-db.mysql.database.azure.com/worldcuppitaco"
                   % (quote_plus("worldcuppitaco"),quote_plus("Copadomundo2022"))  
                      )

con = engine.connect()'''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C0P4_D0_MUND0_P1T4C0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://worldcuppitaco@worldcuppitaco:Copadomundo2022@worldcuppitaco-db.mysql.database.azure.com/worldcuppitaco?ssl_ca=DigiCertGlobalRootG2.crt.pem'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#gerenciamento de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "É necessário fazer login antes para continuar."
login_manager.login_message_category = "alert-warning"

from copadomundo import routes