from marshmallow import Schema, fields  # Importa Schema y fields de marshmallow para definir esquemas de serialización y validación


class PlainItemSchema(Schema):  # Esquema básico para un ítem
    id = fields.Int(dump_only=True)  # Campo id, solo para salida (no se espera en la entrada)
    name = fields.Str(required=True)  # Campo name, requerido
    price = fields.Float(required=True)  # Campo price, requerido


class PlainStoreSchema(Schema):  # Esquema básico para una tienda
    id = fields.Int(dump_only=True)  # Campo id, solo para salida
    name = fields.Str()  # Campo name


class ItemSchema(PlainItemSchema):  # Esquema completo para un ítem, hereda de PlainItemSchema
    store_id = fields.Int(required=True, load_only=True)  # Campo store_id, requerido solo para entrada
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  # Campo anidado store, solo para salida


class ItemUpdateSchema(Schema):  # Esquema para actualizar un ítem (no requiere todos los campos)
    name = fields.Str()  # Campo name, opcional
    price = fields.Float()  # Campo price, opcional


class StoreSchema(PlainStoreSchema):  # Esquema completo para una tienda, hereda de PlainStoreSchema
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)  # Lista de ítems asociados, solo para salida