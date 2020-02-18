from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from . import routes, models
# def create_app():
#     """Construct core application"""
#     app = Flask(__name__, instance_relative_config=False)
#     app.config.from_object("config.Config")
# 
#     with app.app_context():
#         from . import routes
# 
#         db.init_app(app)
#         db.create_all()
#         ma.init_app(app)
# 
#         return app

if __name__ == "__main__":
    app.run()
