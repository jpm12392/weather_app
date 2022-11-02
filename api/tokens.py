import datetime
import jwt
from django.conf import settings


## Generate Access Token for User.
def generate_access_token(user):

    access_token_payload = {'user_id': user, 'token_type': 'access', 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1), 'jti': "b932ba39d8024b39a55b3850129cbd10"}

    return jwt.encode(access_token_payload,settings.SECRET_KEY, algorithm='HS256')

## Generate Refresh Token For User.
def generate_refresh_token(user):
    refresh_token_payload = {'user_id': user, 'token_type': 'refresh', 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7), 'jti': "b932ba39d8024b39a55b3850129cbd10"}

    return jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')