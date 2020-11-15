from os import path, environ
from flask import Flask, render_template, g
from flask_session import Session
from flask_migrate import Migrate
from config import config
from .extensions import db
from .extensions import ma
from .extensions import login_manager
from app.admin.resources.views import admin_bp as admin_blueprint
from app.admin.helpers import handler

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "q7gh8kCFHaa-FsDdG6AtFg"
    login_manager.init_app(app)
    login_manager.login_message = "Debes estar autenticado para ver esta pagina."
    login_manager.login_message_category = "danger"
    login_manager.login_view = "admin.login"

    # Configuracion file_upload
    app.config["UPLOAD_FOLDER"] = 'static/uploads'
    app.config["ALLOWED_EXTENSIONS"] = ["pdf"]
    app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024  # 1mb


    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configuracion db_sqlalchemy
    conf = app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + \
        conf["DB_USER"]+":"+conf["DB_PASS"]+"@" + \
        conf["DB_HOST"]+"/"+conf["DB_NAME"]

    db.init_app(app)
    ma.init_app(app)
    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)

    # Crear el objeto para migraciones
    migrate = Migrate(app, db)
    from app.models import model

    # Registro de Blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/administracion/')

    # Retornar la instancia de app configurada
    return app
