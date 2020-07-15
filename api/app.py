import os

from flask import Flask
from flask_bcrypt import Bcrypt
# from flask_restx import Api
from flask_jwt_extended import JWTManager
import click

from .resources.routes import dnd_api, initialize_routes
from .database.db import db
# from .database.initdb import seed_db

app = Flask(__name__)

appdir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(appdir, ".env")
# app.config.from_envvar('ENV_FILE_LOCATION')
app.config["ENV_FILE_LOCATION"] = env_file
app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb://localhost/dnd_database"
}
app.config["RESTX_MASK_HEADER"] = "Fields"
app.config["ERROR_404_HELP"] = False

# api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

dnd_api.init_app(app)
initialize_routes(dnd_api)
db.init_app(app)

@app.cli.command()
def initdb():
    click.echo("Seeding initial database...")
#     seed_db()


if __name__ == "__main__":
    app.run(debug=True)
