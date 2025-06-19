from flask.views import MethodView  # Importa MethodView para crear vistas basadas en clases en Flask
from flask_smorest import Blueprint, abort  # Importa Blueprint para agrupar rutas y abort para manejar errores
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  # Importa excepciones para manejar errores de base de datos

from db import db  # Importa el objeto db para manejar la base de datos con SQLAlchemy
from models import StoreModel  # Importa el modelo de Store
from schemas import StoreSchema  # Importa el esquema de validación para Store

blp = Blueprint("Stores", "stores", description="Operations on stores")  # Crea un blueprint para agrupar las rutas de stores


@blp.route("/store/<string:store_id>")  # Define la ruta para operaciones sobre una tienda específica
class Store(MethodView):
    @blp.response(200, StoreSchema)  # Responde con el esquema StoreSchema y código 200 si es exitoso
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # Busca la tienda por id o retorna 404 si no existe
        return store  # Devuelve la tienda encontrada

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # Busca la tienda por id o retorna 404 si no existe
        db.session.delete(store)  # Elimina la tienda de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return {"message": "Store deleted"}, 200  # Devuelve un mensaje de confirmación


@blp.route("/store")  # Define la ruta para operaciones sobre la lista de tiendas
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))  # Responde con una lista de tiendas usando StoreSchema
    def get(self):
        return StoreModel.query.all()  # Devuelve todas las tiendas de la base de datos

    @blp.arguments(StoreSchema)  # Valida los datos recibidos con StoreSchema
    @blp.response(201, StoreSchema)  # Responde con el esquema StoreSchema y código 201 si es exitoso
    def post(self, store_data):
        store = StoreModel(**store_data)  # Crea una nueva tienda con los datos recibidos
        try:
            db.session.add(store)  # Agrega la tienda a la sesión de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",  # Si el nombre ya existe, retorna 400
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")  # Si hay otro error, retorna 500

        return store  # Devuelve la tienda creada