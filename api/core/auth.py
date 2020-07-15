from functools import wraps
from flask import jsonify
from ..database.player_models import Player
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, create_access_token, get_jwt_claims
)

jwt = JWTManager()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'admin' not in claims['roles']:
            return jsonify(msg="Administrator access required"), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(username):
    claims = {"roles": []}
    player_collection = Player._get_collection()
    if player_collection.find_one({"admin": {"$exists": True}, "username": username}):
        claims["roles"].append["admin"]
    return claims
