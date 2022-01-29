import json
from flask import Blueprint, Response, request
from controllers import user_controller

bp_api = Blueprint('bp_api', __name__)

# /users
# /users/2
# /users/2/messages
# /users/2/messages/3

@bp_api.get('/users')
def get_all_users():
    api_key = '28511ce952d43b149bc5f0a697592af6c825c8601b4b6ef291c622d03e17c8f6'
    provided_key = request.headers.get('x-api-key', None)
    print(f'Magic~ {provided_key}')
    if provided_key != api_key:
        respone = {
            'Result': 'Api Key Error',
            'Reason': 'No or Wrong api key provided.'
        }
        return Response(json.dumps(respone),)
    users = user_controller.get_all_users()
    cleaned_users = []
    for user in users:
        u = user.__dict__
        del u['_sa_instance_state']
        del u['recv_messages']
        cleaned_users.append(u)

    return Response(json.dumps(cleaned_users), 200, content_type="application/json")