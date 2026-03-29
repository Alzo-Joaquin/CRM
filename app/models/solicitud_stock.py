from datetime import datetime
from app.extensions import db


class SolicitudStock(db.Model):
    __tablename__ = "solicitudes_stock"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="pendiente")
    observaciones = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="solicitudes_stock")
    producto = db.relationship("Producto", backref="solicitudes_stock")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "usuario": self.usuario.nombre if self.usuario else None,
            "producto_id": self.producto_id,
            "producto": self.producto.nombre if self.producto else None,
            "cantidad": self.cantidad,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }