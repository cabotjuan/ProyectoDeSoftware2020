from app.models import users
from os import path, environ
from flask import Flask, render_template, g
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import create_engine
from config import config

#from .admin.resources.admin import admin_bp as admin_blueprint
#from app.admin.resources import admin
#from app.resources import auth
#from app.helpers import handler
#from app.helpers import auth as helper_auth

# db variable initialization
db = SQLAlchemy()

# Inicializacion de Login Manager
login_manager = LoginManager()

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "q7gh8kCFHaa-FsDdG6AtFg"
    login_manager.init_app(app)
    login_manager.login_message = "Debes estar autenticado para ver esta pagina."
    login_manager.login_view = "admin.login"


    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    #Configuracion db_sqlalchemy
    conf = app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" +conf["DB_USER"]+":"+conf["DB_PASS"]+"@"+conf["DB_HOST"]+"/"+conf["DB_NAME"]

    db.init_app(app)
   
    # Funciones que se exportan al contexto de Jinja2
    #app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    #app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    #app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    #app.add_url_rule(
    #    "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    # Rutas de API-rest
    #app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    #app.register_error_handler(404, handler.not_found_error)
    #app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401
    
    # Rutas Administracion

    #app.add_url_rule("/administracion/", "administracion", admin.index)

    #Crear el objeto para migraciones
    migrate = Migrate(app, db)
    #from app.models import users

    # Registro de Blueprint
    #app.register_blueprint(admin_blueprint, url_prefix='/administracion/')
    
    # Retornar la instancia de app configurada
    return app
