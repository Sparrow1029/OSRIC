from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_jwt_extended import JWTManager

from resources.routes import initialize_routes
from database.db import initialize_db

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/dnd_database"
}

initialize_db(app)
initialize_routes(api)

app.run()
