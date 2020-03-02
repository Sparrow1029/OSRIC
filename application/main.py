from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app=app, prefix='/api/v1')
mongo = PyMongo(app)