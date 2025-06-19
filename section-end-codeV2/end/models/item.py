from db import db  # Importa el objeto db para manejar la base de datos con SQLAlchemy


class ItemModel(db.Model):  # Define la clase ItemModel que representa la tabla de items en la base de datos
    __tablename__ = "items"  # Especifica el nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # Columna id, clave primaria, tipo entero
    name = db.Column(db.String(80), unique=False, nullable=False)  # Columna name, tipo string, no única, no puede ser nula
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)  # Columna price, tipo float con 2 decimales, no única, no puede ser nula

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False  # Columna store_id, clave foránea que referencia a la tabla stores, no única, no puede ser nula
    )
    store = db.relationship("StoreModel", back_populates="items")  # Relación con el modelo StoreModel, permite acceder a la tienda asociada y viceversa