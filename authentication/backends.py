from lib2to3.pytree import Base
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix,token = auth_data.decode('utf-8').split(" ")
        # issues when user change username the token is no longer valid 
        # hence the reason for the User.DoesNotExist exception
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.get(username=payload.get('username'))
            return (user, token)
        except (jwt.DecodeError, get_user_model().DoesNotExist) as e:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Your Token has expired!")