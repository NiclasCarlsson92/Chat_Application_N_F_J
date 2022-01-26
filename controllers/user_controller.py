from flask_login import current_user


def get_all_users():
    from models import User
    user = current_user
    return User.query.filter(User.id != user.id).all()
