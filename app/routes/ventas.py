from flask import Blueprint, request, jsonify
from math import ceil
from app.extensions import db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.utils.auth import roles_required
from flask_login import login_required

ventas_bp = Blueprint("ventas", __name__)


@ventas_bp.route("", methods=["POST"])
@login_required
@roles_required("admin", "vendedor")
def crear_venta():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    cliente_id = data.get("cliente_id")
    usuario_id = data.get("usuario_id")
    items = data.get("items")

    if cliente_id is None:
        return jsonify({"error": "El campo 'cliente_id' es obligatorio"}), 400

    if usuario_id is None:
        return jsonify({"error": "El campo 'usuario_id' es obligatorio"}), 400

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "La venta debe tener al menos un item"}), 400

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    if not cliente.activo:
        return jsonify({"error": "El cliente está inactivo"}), 400

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    if not usuario.activo:
        return jsonify({"error": "El usuario está inactivo"}), 400

    productos_procesados = []
    total_venta = 0

    for item in items:
        producto_id = item.get("producto_id")
        cantidad = item.get("cantidad")

        if producto_id is None or cantidad is None:
            return jsonify({"error": "Cada item debe incluir 'producto_id' y 'cantidad'"}), 400

        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            return jsonify({"error": "La cantidad debe ser un número entero válido"}), 400

        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser mayor a cero"}), 400

        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({"error": f"Producto con id {producto_id} no encontrado"}), 404

        if not producto.activo:
            return jsonify({"error": f"El producto '{producto.nombre}' está inactivo"}), 400

        if producto.stock_actual < cantidad:
            return jsonify({
                "error": f"Stock insuficiente para el producto '{producto.nombre}'"
            }), 400

        precio_unitario = float(producto.precio)
        subtotal = precio_unitario * cantidad
        total_venta += subtotal

        productos_procesados.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

    try:
        venta = Venta(
            cliente_id=cliente.id,
            usuario_id=usuario.id,
            total=total_venta,
            estado="registrada"
        )

        db.session.add(venta)
        db.session.flush()

        for item_procesado in productos_procesados:
            producto = item_procesado["producto"]
            cantidad = item_procesado["cantidad"]
            precio_unitario = item_procesado["precio_unitario"]
            subtotal = item_procesado["subtotal"]

            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            )

            db.session.add(detalle)

            producto.stock_actual -= cantidad

        db.session.commit()

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ocurrió un error al registrar la venta"}), 500

    return jsonify({
        "id": venta.id,
        "cliente_id": venta.cliente_id,
        "usuario_id": venta.usuario_id,
        "fecha": venta.fecha.isoformat() if venta.fecha else None,
        "total": float(venta.total),
        "estado": venta.estado,
        "items": [
            {
                "producto_id": item["producto"].id,
                "producto": item["producto"].nombre,
                "cantidad": item["cantidad"],
                "precio_unitario": item["precio_unitario"],
                "subtotal": item["subtotal"]
            }
            for item in productos_procesados
        ]
    }), 201

@ventas_bp.route("", methods=["GET"])
def listar_ventas():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
    except ValueError:
        return jsonify({"error": "Los parámetros 'page' y 'limit' deben ser enteros"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "Los parámetros 'page' y 'limit' deben ser mayores a cero"}), 400

    total = Venta.query.count()
    pages = ceil(total / limit) if total > 0 else 1
    offset = (page - 1) * limit

    ventas = (
        Venta.query
        .order_by(Venta.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    resultado = []
    for venta in ventas:
        resultado.append({
            "id": venta.id,
            "fecha": venta.fecha.isoformat() if venta.fecha else None,
            "total": float(venta.total),
            "estado": venta.estado,
            "cliente_id": venta.cliente_id,
            "cliente": f"{venta.cliente.nombre} {venta.cliente.apellido}",
            "usuario_id": venta.usuario_id,
            "usuario": venta.usuario.nombre,
            "items": [
                {
                    "producto_id": detalle.producto_id,
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": float(detalle.precio_unitario),
                    "subtotal": float(detalle.subtotal)
                }
                for detalle in venta.detalles
            ]
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "results": resultado
    }), 200

@ventas_bp.route("/cliente/<int:cliente_id>", methods=["GET"])
def listar_ventas_por_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)

    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    ventas = Venta.query.filter_by(cliente_id=cliente_id).order_by(Venta.id.asc()).all()

    resultado = []
    for venta in ventas:
        resultado.append({
            "id": venta.id,
            "fecha": venta.fecha.isoformat() if venta.fecha else None,
            "total": float(venta.total),
            "estado": venta.estado,
            "cliente_id": venta.cliente_id,
            "usuario_id": venta.usuario_id,
            "items": [
                {
                    "id": detalle.id,
                    "producto_id": detalle.producto_id,
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": float(detalle.precio_unitario),
                    "subtotal": float(detalle.subtotal)
                }
                for detalle in venta.detalles
            ]
        })

    return jsonify(resultado), 200

@ventas_bp.route("/<int:venta_id>", methods=["GET"])
def obtener_venta(venta_id):
    venta = Venta.query.get(venta_id)

    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404

    return jsonify({
        "id": venta.id,
        "fecha": venta.fecha.isoformat() if venta.fecha else None,
        "total": float(venta.total),
        "estado": venta.estado,
        "cliente_id": venta.cliente_id,
        "usuario_id": venta.usuario_id,
        "items": [
            {
                "id": detalle.id,
                "producto_id": detalle.producto_id,
                "producto": detalle.producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precio_unitario),
                "subtotal": float(detalle.subtotal)
            }
            for detalle in venta.detalles
        ]
    }), 200