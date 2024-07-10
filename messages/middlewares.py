# messages/middlewares.py

import jwt
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@database_sync_to_async
def get_user_from_jwt_payload(payload):
    try:
        user_id = payload.get('user_id')
        if user_id:
            return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
    return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = parse_qs(query_string.decode())

        token_key = query_params.get("token", [None])[0]
        if token_key:
            try:
                payload = jwt.decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user_from_jwt_payload(payload)
            except jwt.ExpiredSignatureError:
                logger.debug("Token has expired")
                user = AnonymousUser()
            except jwt.InvalidTokenError:
                logger.debug("Invalid token")
                user = AnonymousUser()
        else:
            user = AnonymousUser()

        scope["user"] = user

        logger.debug(f"Token: {token_key}, User: {scope['user']}")

        return await self.app(scope, receive, send)
