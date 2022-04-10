from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.player import PlayerModel


class Player(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('goals',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('club_id',
                        type=int,
                        required=True,
                        help="Every player needs a club_id."
                        )

    @jwt_required()
    def get(self, name):
        player = PlayerModel.find_by_name(name)
        if player:
            return player.json()
        return {'message': 'Player not found'}, 404

    def post(self, name):
        if PlayerModel.find_by_name(name):
            return {'message': "A Player with name '{}' already exists.".format(name)}, 400

        data = Player.parser.parse_args()

        player = PlayerModel(name, **data)

        try:
            player.save_to_db()
        except:
            return {"message": "An error occurred adding the player."}, 500

        return player.json(), 201

    def delete(self, name):
        player = PlayerModel.find_by_name(name)
        if player:
            player.delete_from_db()
            return {'message': 'Player removed from club.'}
        return {'message': 'Player not found.'}, 404

    def put(self, name):
        data = Player.parser.parse_args()

        player = PlayerModel.find_by_name(name)

        if player:
            player.price = data['price']
        else:
            player = PlayerModel(name, **data)

        player.save_to_db()

        return player.json()


class PlayerList(Resource):
    def get(self):
        return {'players': list(map(lambda x: x.json(), PlayerModel.query.all()))}
