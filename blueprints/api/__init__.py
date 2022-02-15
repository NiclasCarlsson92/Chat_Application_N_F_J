import json
from functools import wraps
import os
from flask import Blueprint, request, Response
from controllers import user_controller

bp_api = Blueprint('bp_api', __name__)


def authorize(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = os.environ.get('API_KEY')
        provided_key = request.headers.get('x-api-key', None)
        if provided_key != api_key:
            response = {
                'Result': 'Api Key Error',
                'Reason': 'No or Wrong api key provided.'
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return f(*args, **kwargs)
    return wrapper


@bp_api.get('/users')
@authorize
def get_all_users():
    users = user_controller.get_all_users()
    cleaned_users = []
    for user in users:
        u = user.__dict__
        del u['_sa_instance_state']
        del u['recv_messages']
        cleaned_users.append(u)

    return Response(json.dumps(cleaned_users), 200, content_type="application/json")
