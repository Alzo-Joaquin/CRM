from app.extensions import db


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(250), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    categoria = db.relationship("Categoria", back_populates="productos")

    detalles_venta = db.relationship("DetalleVenta", back_populates="producto", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "costo": float(self.costo),
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "activo": self.activo,
            "categoria_id": self.categoria_id,
        }