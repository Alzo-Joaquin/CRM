from flask import Flask, render_template
from app.config import Config
from app.extensions import db, migrate
from app.routes.clientes import clientes_bp
from app.routes.categorias import categorias_bp
from app.routes.productos import productos_bp
from app.routes.usuarios import usuarios_bp
from app.routes.ventas import ventas_bp
from app.routes.dashboard import dashboard_bp

from app import models


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
        )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route("/clientes-ui")
    def clientes_ui():
        return render_template("clientes.html")

    @app.route("/productos-ui")
    def productos_ui():
        return render_template("productos.html")

    @app.route("/ventas-ui")
    def ventas_ui():
        return render_template("ventas.html")
    
    return app