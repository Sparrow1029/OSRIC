from . import app, db
from flask import jsonify, request
from .models import Player, PlayerSchema

player_schema = PlayerSchema()

@app.route("/player/details", methods=["POST"])
def player_details():
    data = request.json
    if data['player_name'] and data['char_name'] and data['strength']:
        existing_char = Player.query.filter_by(char_name=data['char_name']).first()
        if existing_char is not None:
            response = {'message': 'user already exists'}
            return jsonify(response), 403
        new_char = Player(
            player_name=data['player_name'],
            char_name=data['char_name'],
            strength=data['strength']
        )
        db.session.add(new_char)
        db.session.commit()
        response = {'message': 'new player created'}
        return jsonify(response), 202

    response = {'status': 'error', 'message': 'bad request body'}
    return jsonify(response), 400


@app.route("/player/details/<uid>", methods=["GET"])
def get_player_details(uid):
    player = Player.query.filter_by(id=uid).first()
    if player is None:
        response = {"message": "user does not exist"}
        return jsonify(response)
    result = player_schema.dumps(player)
    response = {
        "data": result,
        "status_code": 202
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
