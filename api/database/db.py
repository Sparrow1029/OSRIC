from flask_mongoengine import MongoEngine
# from flask import Flask
# from .character_models import Class, Inventory
# from .object_models import Item, Weapon, Armor, Ability, Spell

db = MongoEngine()

# app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {
#     "db": "dnd_database",
#     "host": "127.0.0.1",
#     "port": 27017
# }

def initialize_db(app):
    db.init_app(app)
    # return db
