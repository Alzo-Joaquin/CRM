from pathlib import Path
from flask import Flask, render_template
from flask_login import login_required, current_user
from flask import abort
from app.config import Config
from app.extensions import db, migrate
from app.routes.clientes import clientes_bp
from app.routes.categorias import categorias_bp
from app.routes.productos import productos_bp
from app.routes.usuarios import usuarios_bp
from app.routes.ventas import ventas_bp
from app.routes.dashboard import dashboard_bp
from app.extensions import db, migrate, login_manager
from app.models.usuario import Usuario
from app.routes.auth import auth_bp
from app.routes.solicitudes_stock import solicitudes_stock_bp
from app import models

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
        static_url_path="/static"
    )
    app.config.from_object(Config) 

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(auth_bp)
    app.register_blueprint(solicitudes_stock_bp, url_prefix="/solicitudes-stock")

    @app.route("/")
    @login_required
    def home():
        if current_user.rol == "admin":
            return render_template("dashboard_admin.html")
        return render_template("dashboard_vendedor.html")
    
    @app.route("/clientes-ui")
    @login_required
    def clientes_ui():
        return render_template("clientes.html")

    @app.route("/productos-ui")
    @login_required
    def productos_ui():
        if current_user.rol != "admin":
            abort(403)
        return render_template("productos.html")

    @app.route("/ventas-ui")
    @login_required
    def ventas_ui():
        return render_template("ventas.html", usuario_actual=current_user)

    @app.route("/usuarios-ui")
    @login_required
    def usuarios_ui():
        if current_user.rol != "admin":
            abort(403)
        return render_template("usuarios.html")
    
    @app.route("/solicitudes-stock-ui")
    @login_required
    def solicitudes_stock_ui():
        if current_user.rol != "vendedor":
            abort(403)
        return render_template("solicitudes_stock.html")
    
    @app.route("/solicitudes-stock-admin-ui")
    @login_required
    def solicitudes_stock_admin_ui():
        if current_user.rol != "admin":
            abort(403)
        return render_template("solicitudes_stock_admin.html")

    return app