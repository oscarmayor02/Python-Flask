from db import db  # Importa el objeto db para manejar la base de datos con SQLAlchemy


class StoreModel(db.Model):  # Define la clase StoreModel que representa la tabla de tiendas en la base de datos
    __tablename__ = "stores"  # Especifica el nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # Columna id, clave primaria, tipo entero
    name = db.Column(db.String(80), unique=True, nullable=False)  # Columna name, tipo string, debe ser única y no puede ser nula

    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"  # Relación con ItemModel, permite acceder a los ítems de la tienda, carga dinámica y elimina ítems asociados si se borra la tienda
    )