from flask import Flask
from flask_restx import Api
from resources.routes import initialize_routes
from database.db import initialize_db

app = Flask(__name__)
api = Api(app)

app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/dnd_database"
}

initialize_db(app)
initialize_routes(api)

app.run()
