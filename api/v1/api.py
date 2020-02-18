from flask import Flask, request, jsonify
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

@app.route('/', methods=["GET"])
def home():
    return """<h1>Welcome to the Thunderdome</h1>

<p>Prototype D&amp;D Character tracking app for campaign management</p>
"""

app.run()
