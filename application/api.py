from main import app, mongo, api
from flask import request, jsonify
from flask_restful import Resource
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
            return _json_convert(db[category].find({'_id': ObjectId(_id)})), 404
        if name:
            return _json_convert(db[category].find({'name': name})), 404

        return _json_convert(db[category].find()), 404


api.add_resource(Equipment, '/equipment')


app.run()
