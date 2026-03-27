from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.cliente import Cliente

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("", methods=["POST"])
def crear_cliente():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    campos_obligatorios = ["nombre", "apellido", "email"]
    for campo in campos_obligatorios:
        if campo not in data or not str(data[campo]).strip():
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    email_existente = Cliente.query.filter_by(email=data["email"]).first()
    if email_existente:
        return jsonify({"error": "Ya existe un cliente con ese email"}), 409

    cliente = Cliente(
        nombre=data["nombre"].strip(),
        apellido=data["apellido"].strip(),
        email=data["email"].strip(),
        telefono=data.get("telefono"),
        direccion=data.get("direccion"),
        activo=True
    )

    db.session.add(cliente)
    db.session.commit()

    return jsonify(cliente.to_dict()), 201


@clientes_bp.route("", methods=["GET"])
def listar_clientes():
    activo_param = request.args.get("activo")

    query = Cliente.query

    if activo_param is not None:
        if activo_param.lower() == "true":
            query = query.filter_by(activo=True)
        elif activo_param.lower() == "false":
            query = query.filter_by(activo=False)
        else:
            return jsonify({"error": "Parámetro 'activo' inválido"}), 400

    clientes = query.order_by(Cliente.id.asc()).all()

    return jsonify([cliente.to_dict() for cliente in clientes]), 200


@clientes_bp.route("/<int:cliente_id>", methods=["GET"])
def obtener_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(cliente.to_dict()), 200


@clientes_bp.route("/<int:cliente_id>", methods=["DELETE"])
def eliminar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    if not cliente.activo:
        return jsonify({"error": "El cliente ya está inactivo"}), 400

    cliente.activo = False

    db.session.commit()

    return jsonify({"mensaje": f"Cliente {cliente_id} dado de baja correctamente"}), 200

@clientes_bp.route("/<int:cliente_id>", methods=["PATCH"])
def actualizar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    campos_permitidos = {"nombre", "apellido", "email", "telefono", "direccion", "activo"}

    for campo in data:
        if campo not in campos_permitidos:
            return jsonify({"error": f"El campo '{campo}' no es válido para actualizar"}), 400

    if "nombre" in data:
        nombre = str(data["nombre"]).strip()
        if not nombre:
            return jsonify({"error": "El campo 'nombre' no puede estar vacío"}), 400
        cliente.nombre = nombre

    if "apellido" in data:
        apellido = str(data["apellido"]).strip()
        if not apellido:
            return jsonify({"error": "El campo 'apellido' no puede estar vacío"}), 400
        cliente.apellido = apellido

    if "email" in data:
        email = str(data["email"]).strip()
        if not email:
            return jsonify({"error": "El campo 'email' no puede estar vacío"}), 400

        cliente_con_mismo_email = Cliente.query.filter(
            Cliente.email == email,
            Cliente.id != cliente.id
        ).first()

        if cliente_con_mismo_email:
            return jsonify({"error": "Ya existe otro cliente con ese email"}), 409

        cliente.email = email

    if "telefono" in data:
        telefono = data["telefono"]
        cliente.telefono = str(telefono).strip() if telefono is not None else None

    if "direccion" in data:
        direccion = data["direccion"]
        cliente.direccion = str(direccion).strip() if direccion is not None else None

    if "activo" in data:
        if not isinstance(data["activo"], bool):
            return jsonify({"error": "El campo 'activo' debe ser booleano"}), 400
        cliente.activo = data["activo"]

    db.session.commit()

    return jsonify(cliente.to_dict()), 200