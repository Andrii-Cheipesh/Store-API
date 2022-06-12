from models.user import UserModel


def authenticate(username, password):
    # method to retrieve user by username
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    # method to retrieve user by id
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
