from database import init_db
# from mongoengine import connect
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
import datetime
# from flask_graphql_auth import GraphQLAuth
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_claims
)
from schema import schema
from models import Player

app = Flask(__name__)
app.debug = True
app.config["JWT_SECRET_KEY"] = "Gh4fdy7fdqAA8fdfsa80yUt=="

jwt = JWTManager(app)
# GraphQLAuth(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        "user_id": identity,
        "claims": ["create", "update", "delete"]
    }


# For production
app.add_url_rule(
    "/graphql",
    view_func=jwt_required(
        GraphQLView.as_view("graphql", schema=schema)
       )
    )

# For testing
app.add_url_rule(
    "/graphqltesting",
    view_func=GraphQLView.as_view("graphqltesting", schema=schema, graphiql=True))


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if None in [username, password]:
        return jsonify({ "message": "Invalid request." }), 400

    player = Player.objects.get(username=username)

    if not player.check_password_hash(password):
        return jsonify({ "message": "Poop on YOU!" }), 401

    expires = datetime.timedelta(7)
    ret = {"access_token": create_access_token(str(player.id), expires_delta=expires)}
    return jsonify(ret), 200


@app.route("/protected", methods=["GET"])
@jwt_required
def protected():
    claims = get_jwt_claims()
    return jsonify({
        "user_id_is": claims["user_id"] ,
        "claims_are": claims["claims"]
    }), 200


if __name__ == "__main__":
    init_db()
    app.run()
