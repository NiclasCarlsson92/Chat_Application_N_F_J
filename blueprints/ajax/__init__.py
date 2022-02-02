import json
from flask import Blueprint, Response
from controllers.message_controller import get_unread_msg_count

bp_ajax = Blueprint('bp_ajax', __name__)


@bp_ajax.get('/get_message_count')
def get_message_count():
    msg_count = get_unread_msg_count()
    messages = {
        "unreadMessageCount": msg_count
    }

    return Response(json.dumps(messages), 200, content_type='application/json')
