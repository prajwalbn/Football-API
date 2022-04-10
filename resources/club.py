from flask_restful import Resource
from models.clubs import ClubModel


class Club(Resource):
    def get(self, name):
        club = ClubModel.find_by_name(name)
        if club:
            return club.json()
        return {'message': 'Club not found'}, 404

    def post(self, name):
        if ClubModel.find_by_name(name):
            return {'message': "A football club with name '{}' already exists.".format(name)}, 400

        club = ClubModel(name)
        try:
            club.save_to_db()
        except:
            return {"message": "An error occurred creating the a club."}, 500

        return club.json(), 201

    def delete(self, name):
        club = ClubModel.find_by_name(name)
        if club:
            club.delete_from_db()

        return {'message': 'Club removed'}


class ClubList(Resource):
    def get(self):
        return {'clubs': list(map(lambda x: x.json(), ClubModel.query.all()))}
