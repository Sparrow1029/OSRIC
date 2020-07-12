from flask import Response, request
from database.class_models import Class
# from bson import ObjectId
from flask_restx import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of class")
parser.add_argument("id", help="Mongodb ObjectId")


class ClassesApi(Resource):
    # args = parser.parse_args()
    def get(self):
        classes = Class.objects().to_json()
        return Response(classes, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        clss = Class(**body).save()
        id_ = clss.id
        return {'id': str(id_)}, 200


class ClassApi(Resource):
    # def put(self, **kwargs):
    #     body = request.get_json()
    #     if "id" in kwargs:
    #         Class.objects.get(id=kwargs["id"]).update(**body)
    #     elif "name" in kwargs:
    #         Class.objects.get(classname=kwargs["name"]).update(**body)
    #     return '', 204

    def get(self, **kwargs):
        # args = parser.parse_args()
        if "id" in kwargs:
            clss= Class.objects.get(id=kwargs["id"]).to_json()
        elif "name" in kwargs:
            clss = Class.objects.get(classname=kwargs["name"]).to_json()
        return Response(clss, mimetype="application/json", status=200)
