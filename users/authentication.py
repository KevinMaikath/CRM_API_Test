from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


# Time left to expire.
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.AUTH_TOKEN_EXPIRY_TIME_SECONDS) - time_elapsed
    return left_time


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# If the token is expired, it will be deleted and a new one will be created.
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


# ________________________________________________
# DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Check if a token is invalid or expired.
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired = is_token_expired(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")

        return token.user, token
