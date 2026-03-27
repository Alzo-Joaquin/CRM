from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.categoria import Categoria

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("", methods=["POST"])
def crear_categoria():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Debe enviar un body en formato JSON"}), 400

    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not nombre or not str(nombre).strip():
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    categoria_existente = Categoria.query.filter_by(nombre=nombre.strip()).first()
    if categoria_existente:
        return jsonify({"error": "Ya existe una categoría con ese nombre"}), 409

    categoria = Categoria(
        nombre=nombre.strip(),
        descripcion=descripcion.strip() if descripcion else None
    )

    db.session.add(categoria)
    db.session.commit()

    return jsonify(categoria.to_dict()), 201


@categorias_bp.route("", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.order_by(Categoria.id.asc()).all()
    return jsonify([categoria.to_dict() for categoria in categorias]), 200