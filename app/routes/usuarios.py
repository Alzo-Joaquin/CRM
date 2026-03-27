from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.usuario import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("", methods=["POST"])
def crear_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    campos_obligatorios = ["nombre", "email", "rol"]
    for campo in campos_obligatorios:
        if campo not in data or not str(data[campo]).strip():
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    email = data["email"].strip()

    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"error": "Ya existe un usuario con ese email"}), 409

    usuario = Usuario(
        nombre=data["nombre"].strip(),
        email=email,
        rol=data["rol"].strip(),
        activo=True
    )

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.to_dict()), 201


@usuarios_bp.route("", methods=["GET"])
def listar_usuarios():
    activo_param = request.args.get("activo")

    query = Usuario.query

    if activo_param is not None:
        if activo_param.lower() == "true":
            query = query.filter_by(activo=True)
        elif activo_param.lower() == "false":
            query = query.filter_by(activo=False)
        else:
            return jsonify({"error": "Parámetro 'activo' inválido"}), 400

    usuarios = query.order_by(Usuario.id.asc()).all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


@usuarios_bp.route("/<int:usuario_id>", methods=["GET"])
def obtener_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario.to_dict()), 200

@usuarios_bp.route("/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not usuario.activo:
        return jsonify({"error": "El usuario ya está inactivo"}), 400

    usuario.activo = False
    db.session.commit()

    return jsonify({
        "mensaje": f"Usuario {usuario_id} dado de baja correctamente"
    }), 200