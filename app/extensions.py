from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Tenes que iniciar sesión para acceder.'
login_manager.login_message_category = 'warning'

socketio = SocketIO(cors_allowed_origins='*')