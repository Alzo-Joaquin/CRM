from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    fecha_alta = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    activo = db.Column(db.Boolean, nullable=False, default=True)

    ventas = db.relationship("Venta", back_populates="cliente", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "fecha_alta": self.fecha_alta.isoformat() if self.fecha_alta else None,
            "activo": self.activo,
        }