from datetime import date
from flask import Blueprint, jsonify
from sqlalchemy import func

from app.extensions import db
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/kpis", methods=["GET"])
def obtener_kpis_dashboard():
    total_clientes = db.session.query(func.count(Cliente.id)).scalar() or 0
    total_productos = db.session.query(func.count(Producto.id)).scalar() or 0

    total_unidades_vendidas = (
        db.session.query(func.coalesce(func.sum(DetalleVenta.cantidad), 0)).scalar() or 0
    )

    hoy = date.today()

    total_ventas_hoy = (
        db.session.query(func.count(Venta.id))
        .filter(func.date(Venta.fecha) == hoy)
        .scalar()
        or 0
    )

    return jsonify({
        "clientes": total_clientes,
        "productos": total_productos,
        "unidades_vendidas": int(total_unidades_vendidas),
        "ventas_del_dia": total_ventas_hoy
    }), 200