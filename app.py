

from flask import Flask
from flask_login import LoginManager
from home.views import home_blueprint
from auth.views import auth_blueprint

##from vistas.views import vistas_blueprint
from error_pages.handlers import error_pages
from auth.models import get_user_by_id
#from flask_sqlalchemy import SQLAlchem
#from .models import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['ENV'] = 'development'



RECAPTCHA_SITE_KEY = '6Lfd2RYnAAAAAKzIBvjcVwnWxJ3Qz2TKuVPph4BR'
RECAPTCHA_SECRET_KEY = '6Lfd2RYnAAAAAKzIBvjcVwnWxJ3Qz2TKuVPph4BR'


######### Configuracion de Flask Login ##########
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

@login_manager.user_loader
def load_user(ID):
    return get_user_by_id(ID)

################# Apps ##################
app.register_blueprint(home_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(error_pages)


#db.init_app(app)
 
if __name__ == '__main__':
    app.run(debug=True)

