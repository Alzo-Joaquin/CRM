from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.producto import Producto
from app.models.categoria import Categoria
from flask_login import login_required
from app.utils.auth import roles_required

productos_bp = Blueprint("productos", __name__)


@productos_bp.route("", methods=["POST"])
@login_required
@roles_required("admin")
def crear_producto():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    campos_obligatorios = [
        "nombre",
        "precio",
        "costo",
        "stock_actual",
        "stock_minimo",
        "categoria_id"
    ]

    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    nombre = str(data["nombre"]).strip()
    if not nombre:
        return jsonify({"error": "El campo 'nombre' no puede estar vacío"}), 400

    categoria = Categoria.query.get(data["categoria_id"])
    if not categoria:
        return jsonify({"error": "La categoría indicada no existe"}), 404

    try:
        precio = float(data["precio"])
        costo = float(data["costo"])
        stock_actual = int(data["stock_actual"])
        stock_minimo = int(data["stock_minimo"])
    except (ValueError, TypeError):
        return jsonify({"error": "Precio, costo y stocks deben tener formato numérico válido"}), 400

    if precio < 0 or costo < 0:
        return jsonify({"error": "Precio y costo no pueden ser negativos"}), 400

    if stock_actual < 0 or stock_minimo < 0:
        return jsonify({"error": "Los valores de stock no pueden ser negativos"}), 400

    producto = Producto(
        nombre=nombre,
        descripcion=data.get("descripcion"),
        precio=precio,
        costo=costo,
        stock_actual=stock_actual,
        stock_minimo=stock_minimo,
        categoria_id=data["categoria_id"],
        activo=True
    )

    db.session.add(producto)
    db.session.commit()

    return jsonify(producto.to_dict()), 201


@productos_bp.route("", methods=["GET"])
def listar_productos():
    activo_param = request.args.get("activo")

    query = Producto.query

    if activo_param is not None:
        if activo_param.lower() == "true":
            query = query.filter_by(activo=True)
        elif activo_param.lower() == "false":
            query = query.filter_by(activo=False)
        else:
            return jsonify({"error": "Parámetro 'activo' inválido"}), 400

    productos = query.order_by(Producto.id.asc()).all()
    return jsonify([
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": float(producto.precio),
            "costo": float(producto.costo),
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "activo": producto.activo,
            "categoria_id": producto.categoria_id,
            "categoria": producto.categoria.nombre if producto.categoria else None
        }
        for producto in productos
    ]), 200


@productos_bp.route("/stock-bajo", methods=["GET"])
def listar_productos_stock_bajo():
    productos = Producto.query.filter(Producto.stock_actual <= Producto.stock_minimo).order_by(Producto.id.asc()).all()
    return jsonify([producto.to_dict() for producto in productos]), 200

@productos_bp.route("/<int:producto_id>/stock", methods=["PATCH"])
@login_required
@roles_required("admin")
def actualizar_stock_producto(producto_id):
    producto = Producto.query.get(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    tiene_stock_actual = "stock_actual" in data
    tiene_cantidad = "cantidad" in data

    if tiene_stock_actual and tiene_cantidad:
        return jsonify({
            "error": "Debe enviar solo uno de estos campos: 'stock_actual' o 'cantidad'"
        }), 400

    if not tiene_stock_actual and not tiene_cantidad:
        return jsonify({
            "error": "Debe enviar 'stock_actual' o 'cantidad'"
        }), 400

    if tiene_stock_actual:
        try:
            nuevo_stock = int(data["stock_actual"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'stock_actual' debe ser un entero válido"}), 400

        if nuevo_stock < 0:
            return jsonify({"error": "El stock no puede ser negativo"}), 400

        producto.stock_actual = nuevo_stock

    if tiene_cantidad:
        try:
            cantidad = int(data["cantidad"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'cantidad' debe ser un entero válido"}), 400

        nuevo_stock = producto.stock_actual + cantidad

        if nuevo_stock < 0:
            return jsonify({"error": "La operación dejaría el stock en un valor negativo"}), 400

        producto.stock_actual = nuevo_stock

    db.session.commit()

    return jsonify({
        "mensaje": "Stock actualizado correctamente",
        "producto_id": producto.id,
        "nombre": producto.nombre,
        "stock_actual": producto.stock_actual
    }), 200

@productos_bp.route("/<int:producto_id>", methods=["DELETE"])
@login_required
@roles_required("admin")
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    if not producto.activo:
        return jsonify({"error": "El producto ya está inactivo"}), 400

    producto.activo = False
    db.session.commit()

    return jsonify({
        "mensaje": f"Producto {producto_id} dado de baja correctamente"
    }), 200

@productos_bp.route("/<int:producto_id>", methods=["PATCH"])
@login_required
@roles_required("admin")
def actualizar_producto(producto_id):
    producto = Producto.query.get(producto_id)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    campos_permitidos = {
        "nombre",
        "descripcion",
        "precio",
        "costo",
        "stock_minimo",
        "categoria_id",
        "activo"
    }

    for campo in data:
        if campo not in campos_permitidos:
            return jsonify({"error": f"El campo '{campo}' no es válido para actualizar"}), 400

    if "nombre" in data:
        nombre = str(data["nombre"]).strip()
        if not nombre:
            return jsonify({"error": "El campo 'nombre' no puede estar vacío"}), 400
        producto.nombre = nombre

    if "descripcion" in data:
        descripcion = data["descripcion"]
        producto.descripcion = str(descripcion).strip() if descripcion is not None else None

    if "precio" in data:
        try:
            precio = float(data["precio"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'precio' debe ser numérico"}), 400

        if precio < 0:
            return jsonify({"error": "El precio no puede ser negativo"}), 400

        producto.precio = precio

    if "costo" in data:
        try:
            costo = float(data["costo"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'costo' debe ser numérico"}), 400

        if costo < 0:
            return jsonify({"error": "El costo no puede ser negativo"}), 400

        producto.costo = costo

    if "stock_minimo" in data:
        try:
            stock_minimo = int(data["stock_minimo"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'stock_minimo' debe ser un entero"}), 400

        if stock_minimo < 0:
            return jsonify({"error": "El stock mínimo no puede ser negativo"}), 400

        producto.stock_minimo = stock_minimo

    if "categoria_id" in data:
        try:
            categoria_id = int(data["categoria_id"])
        except (ValueError, TypeError):
            return jsonify({"error": "El campo 'categoria_id' debe ser un entero"}), 400

        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({"error": "La categoría indicada no existe"}), 404

        producto.categoria_id = categoria_id

    if "activo" in data:
        if not isinstance(data["activo"], bool):
            return jsonify({"error": "El campo 'activo' debe ser booleano"}), 400
        producto.activo = data["activo"]

    db.session.commit()

    return jsonify(producto.to_dict()), 200