from flask_login import current_user

from controllers.user_controller import get_user_by_id


def create_message(title, body, receiver_id):
    from models import Message
    user = current_user
    message = Message(title=title, body=body, sender_id=user.id)

    receiver_id = int(receiver_id)
    receiver = get_user_by_id(receiver_id)
    message.receivers.append(receiver)
    from app import db
    db.session.add(message)
    db.session.commit()

def get_user_messages():
    return current_user.recv_messages


