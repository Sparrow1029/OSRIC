from main import app, mongo, api
from flask import request, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import _json_convert
from bson.objectid import ObjectId


@app.route('/', methods=["GET"])
def home():
    return """<h1>Welcome to the Thunderdome</h1>

<p>Prototype D&amp;D Character tracking app for campaign management</p>
"""

class Equipment(Resource):
    def get(self):
        db = mongo.cx["equipment"]
        category = request.args.get('category', "")
        name = request.args.get('name', "")
        _id = request.args.get('id', "")

        if not category:
            return jsonify("Please select a category")
        if _id and not name and ObjectId.is_valid(_id):
            return _json_convert(db[category].find({'_id': ObjectId(_id)})), 200
        if name:
            return _json_convert(db[category].find({'name': name})), 200

        return _json_convert(db[category].find()), 200


class CharacterForm(Resource):
    def __init__(self):
        fields = [
            "player", "char_name", "race", "class",
        ]
        stats = [
            "str", "dex", "con", "int", "wis", "cha",
        ]
        self.parser = reqparse.RequestParser()
        for field in fields:
            self.parser.add_argument(field, type=str, required=True)
        for stat in stats:
            self.parser.add_argument(stat, type=int, required=True)


    def post(self):
        # db = mongo.cx["players"]
        args = self.parser.parse_args()
        li = ""
        for k, v in args.items():
            li += f"<li>{k}: {v}</li>"
        return f"<html><body><ul>{li}</ul></body></html>"


api.add_resource(Equipment, '/equipment')
api.add_resource(CharacterForm, '/character')

app.run()
