from hmac import compare_digest
from models.manager import ManagerModel


def authenticate(username, password):
    user = ManagerModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return ManagerModel.find_by_id(user_id)
