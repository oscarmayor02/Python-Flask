from flask import Flask  # Importa la clase principal de Flask para crear la aplicación web
from flask_smorest import Api  # Importa la clase Api de flask_smorest para crear APIs RESTful

from db import db  # Importa el objeto db para manejar la base de datos con SQLAlchemy

import models  # Importa los modelos de la base de datos (definiciones de tablas)

from resources.item import blp as ItemBlueprint  # Importa el blueprint de los endpoints de items
from resources.store import blp as StoreBlueprint  # Importa el blueprint de los endpoints de stores


def create_app(db_url=None):  # Función para crear y configurar la aplicación Flask
    app = Flask(__name__)  # Crea una instancia de la aplicación Flask

    # Configuración de la API y la documentación
    app.config["API_TITLE"] = "Stores REST API"  # Título de la API
    app.config["API_VERSION"] = "v1"  # Versión de la API
    app.config["OPENAPI_VERSION"] = "3.0.3"  # Versión de OpenAPI para la documentación
    app.config["OPENAPI_URL_PREFIX"] = "/"  # Prefijo de las rutas de la documentación
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Ruta para Swagger UI
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # URL de los recursos de Swagger UI

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"  # URI de la base de datos
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desactiva el seguimiento de cambios para ahorrar recursos
    app.config["PROPAGATE_EXCEPTIONS"] = True  # Permite que las excepciones se propaguen

    db.init_app(app)  # Inicializa la base de datos con la app

    api = Api(app)  # Crea la instancia de la API y la asocia a la app

    with app.app_context():  # Abre el contexto de la aplicación
        db.create_all()  # Crea todas las tablas definidas en los modelos

    api.register_blueprint(ItemBlueprint)  # Registra el blueprint de items en la API
    api.register_blueprint(StoreBlueprint)  # Registra el blueprint de stores en la API

    return app  # Devuelve la aplicación configurada