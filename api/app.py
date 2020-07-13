from flask import Flask
from flask_bcrypt import Bcrypt
# from flask_restx import Api
from flask_jwt_extended import JWTManager

from resources.routes import dnd_api, initialize_routes
from database.db import initialize_db

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

# api = Api(app)
initialize_routes(dnd_api)
dnd_api.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/dnd_database"
}
app.config["RESTX_MASK_HEADER"] = "Fields"
app.config["ERROR_404_HELP"] = False

initialize_db(app)

if __name__ == "__main__":
    app.run(debug=True)
