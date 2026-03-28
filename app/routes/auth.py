from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.models.usuario import Usuario
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash("Usuario o contraseña incorrectos.", "error")
            return render_template("login.html")

        if not usuario.activo:
            flash("El usuario está inactivo.", "error")
            return render_template("login.html")

        if not usuario.check_password(password):
            flash("Usuario o contraseña incorrectos.", "error")
            return render_template("login.html")

        login_user(usuario)
        return redirect(url_for("home"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirmar_password = request.form.get("confirmar_password", "").strip()

        if not nombre:
            flash("El nombre es obligatorio.", "error")
            return render_template("register.html")

        if not email:
            flash("El email es obligatorio.", "error")
            return render_template("register.html")

        if not password:
            flash("La contraseña es obligatoria.", "error")
            return render_template("register.html")

        if password != confirmar_password:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("register.html")

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("Ya existe un usuario con ese email.", "error")
            return render_template("register.html")

        usuario = Usuario(
            nombre=nombre,
            email=email,
            rol="vendedor",
            activo=True
        )
        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("auth.register_success"))

    return render_template("register.html")

@auth_bp.route("/register-success")
def register_success():
    return render_template("register_success.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))