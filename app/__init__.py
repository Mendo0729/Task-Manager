from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.utils.db import db  # Importamos desde tu ubicación personalizada
import logging
from logging.handlers import RotatingFileHandler
import os
import socket
import json

# Extensiones (excepto db que ya está en utils/db.py)
login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()

class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.host_ip = socket.gethostbyname(socket.gethostname())

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "ip": self.host_ip
        }
        return json.dumps(log_data)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicialización ORDENADA con la app
    db.init_app(app)  # SQLAlchemy desde utils/db.py
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configuración de LoginManager
    login_manager.login_view = None
    login_manager.session_protection = "strong"

    # Configuración de logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1024*1024, backupCount=5)
    file_handler.setFormatter(JSONFormatter())
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Registrar blueprints
    from app.routes.api.auth_api import auth_api as auth_blueprint
    from app.routes.api.task_api import api_tasks as task_blueprint
    from app.routes.web.auth_web import auth_views
    from app.routes.web.task_web import task_views
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(auth_views)
    app.register_blueprint(task_views)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Crear tablas en contexto
    with app.app_context():
        if app.config['DEBUG']:
            db.create_all()

    return app