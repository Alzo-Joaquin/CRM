from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db, socketio
from app.models.producto import Producto
from app.models.solicitud_stock import SolicitudStock
from app.utils.auth import roles_required

solicitudes_stock_bp = Blueprint("solicitudes_stock", __name__)


@solicitudes_stock_bp.route("", methods=["POST"])
@login_required
@roles_required("vendedor", "admin")
def crear_solicitud_stock():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    producto_id = data.get("producto_id")
    cantidad = data.get("cantidad")
    observaciones = data.get("observaciones", "").strip()

    if producto_id is None:
        return jsonify({"error": "El campo 'producto_id' es obligatorio"}), 400

    if cantidad is None:
        return jsonify({"error": "El campo 'cantidad' es obligatorio"}), 400

    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número entero válido"}), 400

    if cantidad <= 0:
        return jsonify({"error": "La cantidad debe ser mayor a cero"}), 400

    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    solicitud = SolicitudStock(
        usuario_id=current_user.id,
        producto_id=producto.id,
        cantidad=cantidad,
        estado="pendiente",
        observaciones=observaciones or None
    )

    db.session.add(solicitud)
    db.session.commit()

    socketio.emit(
        "solicitud_stock_nueva",
        {
            "id": solicitud.id,
            "producto": solicitud.producto.nombre if solicitud.producto else None,
            "cantidad": solicitud.cantidad,
            "usuario": current_user.nombre,
            "estado": solicitud.estado,
        },
        room="admins"
    )

    return jsonify(solicitud.to_dict()), 201


@solicitudes_stock_bp.route("", methods=["GET"])
@login_required
@roles_required("vendedor", "admin")
def listar_solicitudes_stock():
    query = SolicitudStock.query

    if current_user.rol != "admin":
        query = query.filter(SolicitudStock.usuario_id == current_user.id)

    solicitudes = query.order_by(SolicitudStock.id.desc()).all()

    return jsonify([solicitud.to_dict() for solicitud in solicitudes]), 200

@solicitudes_stock_bp.route("/pendientes-count", methods=["GET"])
@login_required
@roles_required("admin")
def contar_solicitudes_pendientes():
    total = (
        db.session.query(func.count(SolicitudStock.id))
        .filter(SolicitudStock.estado == "pendiente")
        .scalar()
        or 0
    )

    return jsonify({"pendientes": total}), 200

@solicitudes_stock_bp.route("/<int:solicitud_id>/aprobar", methods=["PATCH"])
@login_required
@roles_required("admin")
def aprobar_solicitud_stock(solicitud_id):
    solicitud = SolicitudStock.query.get(solicitud_id)

    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    if solicitud.estado != "pendiente":
        return jsonify({"error": "Solo se pueden aprobar solicitudes pendientes"}), 400

    producto = solicitud.producto
    if not producto:
        return jsonify({"error": "Producto asociado no encontrado"}), 404

    try:
        producto.stock_actual += solicitud.cantidad
        solicitud.estado = "aprobada"

        db.session.commit()

        socketio.emit(
            "solicitud_stock_actualizada",
            {
                "id": solicitud.id,
                "estado": solicitud.estado,
                "producto": producto.nombre,
                "cantidad": solicitud.cantidad,
                "usuario_id": solicitud.usuario_id,
                "stock_actual": producto.stock_actual,
            },
            room="admins"
        )

        socketio.emit(
            "solicitud_stock_actualizada",
            {
                "id": solicitud.id,
                "estado": solicitud.estado,
                "producto": producto.nombre,
                "cantidad": solicitud.cantidad,
                "usuario_id": solicitud.usuario_id,
                "stock_actual": producto.stock_actual,
            },
            room=f"vendedor_{solicitud.usuario_id}"
        )

        return jsonify({
            "mensaje": "Solicitud aprobada correctamente",
            "solicitud": solicitud.to_dict(),
            "stock_actual": producto.stock_actual
        }), 200


    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ocurrió un error al aprobar la solicitud"}), 500


@solicitudes_stock_bp.route("/<int:solicitud_id>/rechazar", methods=["PATCH"])
@login_required
@roles_required("admin")
def rechazar_solicitud_stock(solicitud_id):
    solicitud = SolicitudStock.query.get(solicitud_id)

    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    if solicitud.estado != "pendiente":
        return jsonify({"error": "Solo se pueden rechazar solicitudes pendientes"}), 400

    try:
        solicitud.estado = "rechazada"

        db.session.commit()

        socketio.emit(
            "solicitud_stock_actualizada",
            {
                "id": solicitud.id,
                "estado": solicitud.estado,
                "producto": solicitud.producto.nombre if solicitud.producto else None,
                "cantidad": solicitud.cantidad,
                "usuario_id": solicitud.usuario_id,
            },
            room="admins"
        )

        socketio.emit(
            "solicitud_stock_actualizada",
            {
                "id": solicitud.id,
                "estado": solicitud.estado,
                "producto": solicitud.producto.nombre if solicitud.producto else None,
                "cantidad": solicitud.cantidad,
                "usuario_id": solicitud.usuario_id,
            },
            room=f"vendedor_{solicitud.usuario_id}"
        )

        return jsonify({
            "mensaje": "Solicitud rechazada correctamente",
            "solicitud": solicitud.to_dict()
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Ocurrió un error al rechazar la solicitud"}), 500

@solicitudes_stock_bp.route("/mis-notificaciones", methods=["GET"])
@login_required
@roles_required("vendedor")
def mis_notificaciones_solicitudes_stock():
    solicitudes = (
        SolicitudStock.query
        .filter(SolicitudStock.usuario_id == current_user.id)
        .filter(
            (SolicitudStock.estado == "aprobada") |
            (SolicitudStock.estado == "rechazada")
        )
        .order_by(SolicitudStock.id.desc())
        .limit(5)
        .all()
    )

    # FILTRAMOS SOLO APROBADAS NO RECIBIDAS + TODAS LAS RECHAZADAS
    resultado = []

    for s in solicitudes:
        if s.recibido_por_vendedor:
            continue

        resultado.append(s.to_dict())

    return jsonify(resultado), 200

@solicitudes_stock_bp.route("/<int:solicitud_id>/recibido", methods=["PATCH"])
@login_required
@roles_required("vendedor")
def marcar_solicitud_como_recibida(solicitud_id):
    solicitud = SolicitudStock.query.get(solicitud_id)

    if not solicitud:
        return jsonify({"error": "Solicitud no encontrada"}), 404

    if solicitud.usuario_id != current_user.id:
        return jsonify({"error": "No autorizado"}), 403

    if solicitud.estado not in ["aprobada", "rechazada"]:
        return jsonify({"error": "Solo solicitudes procesadas pueden marcarse como recibidas"}), 400

    try:
        solicitud.recibido_por_vendedor = True
        db.session.commit()

        socketio.emit(
            "solicitud_stock_recibida",
            {
                "id": solicitud.id,
                "usuario_id": solicitud.usuario_id,
            },
            room="admins"
        )

        socketio.emit(
            "solicitud_stock_recibida",
            {
                "id": solicitud.id,
                "usuario_id": solicitud.usuario_id,
            },
            room=f"vendedor_{solicitud.usuario_id}"
        )

        return jsonify({"ok": True}), 200

    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        return jsonify({"error": "Error interno"}), 500