from app.extensions import db


class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    estado = db.Column(db.String(50), nullable=False, default="registrada")

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="ventas")
    usuario = db.relationship("Usuario", back_populates="ventas")
    detalles = db.relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total": float(self.total),
            "estado": self.estado,
            "cliente_id": self.cliente_id,
            "usuario_id": self.usuario_id,
        }