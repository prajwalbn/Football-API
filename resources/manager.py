from flask_restful import Resource, reqparse
from models.manager import ManagerModel


class ManagerRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = ManagerRegister.parser.parse_args()

        if ManagerModel.find_by_username(data['username']):
            return {"message": "A Football Manager with that username already exists"}, 400

        manager = ManagerModel(data['username'], data['password'])
        manager.save_to_db()

        return {"message": "Football Manager created successfully."}, 201
