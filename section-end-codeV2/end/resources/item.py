from flask.views import MethodView  # Importa MethodView para crear vistas basadas en clases en Flask
from flask_smorest import Blueprint, abort  # Importa Blueprint para agrupar rutas y abort para manejar errores
from sqlalchemy.exc import SQLAlchemyError  # Importa la excepción para manejar errores de la base de datos

from db import db  # Importa el objeto db para manejar la base de datos con SQLAlchemy
from models import ItemModel  # Importa el modelo de Item
from schemas import ItemSchema, ItemUpdateSchema  # Importa los esquemas de validación para Item

blp = Blueprint("Items", "items", description="Operations on items")  # Crea un blueprint para agrupar las rutas de items


@blp.route("/item/<string:item_id>")  # Define la ruta para operaciones sobre un item específico
class Item(MethodView):
    @blp.response(200, ItemSchema)  # Responde con el esquema ItemSchema y código 200 si es exitoso
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  # Busca el item por id o retorna 404 si no existe
        return item  # Devuelve el item encontrado

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  # Busca el item por id o retorna 404 si no existe
        db.session.delete(item)  # Elimina el item de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return {"message": "Item deleted."}  # Devuelve un mensaje de confirmación

    @blp.arguments(ItemUpdateSchema)  # Valida los datos recibidos con ItemUpdateSchema
    @blp.response(200, ItemSchema)  # Responde con el esquema ItemSchema y código 200 si es exitoso
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)  # Busca el item por id

        if item:
            item.price = item_data["price"]  # Actualiza el precio si el item existe
            item.name = item_data["name"]  # Actualiza el nombre si el item existe
        else:
            item = ItemModel(id=item_id, **item_data)  # Si no existe, crea un nuevo item con ese id y datos

        db.session.add(item)  # Agrega el item (nuevo o actualizado) a la sesión de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos

        return item  # Devuelve el item actualizado o creado


@blp.route("/item")  # Define la ruta para operaciones sobre la lista de items
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))  # Responde con una lista de items usando ItemSchema
    def get(self):
        return ItemModel.query.all()  # Devuelve todos los items de la base de datos

    @blp.arguments(ItemSchema)  # Valida los datos recibidos con ItemSchema
    @blp.response(201, ItemSchema)  # Responde con el esquema ItemSchema y código 201 si es exitoso
    def post(self, item_data):
        item = ItemModel(**item_data)  # Crea un nuevo item con los datos recibidos

        try:
            db.session.add(item)  # Agrega el item a la sesión de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")  # Si hay error, retorna 500

        return item  # Devuelve el item creado