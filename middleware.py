from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions

from . import tokens


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth_header, str):
        # Work around django test client oddness
        auth_header = auth_header.encode(HTTP_HEADER_ENCODING)
    return auth_header


class Authentication(BaseAuthentication):
    """
    Simple JWT token authentication.
    Clients should authenticate by passing the JWT token in the "Authorization"
    HTTP header, prepended with the string "Bearer".  For example:
        Authorization: Bearer 401f7ac837da42b97f613d7.89819ff93537bee6a...sdfe
    """

    keyword = 'Bearer'

    def authenticate(self, request):
        header = get_authorization_header(request).split()

        if not header or header[0].lower() != self.keyword.lower().encode():
            return None

        if len(header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = header[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_token(token)

    def authenticate_token(self, token):
        """Validate token if valid returns user object"""

        model = get_user_model()

        try:
            claims = tokens.is_valid(token)
        except BaseException:
            raise exceptions.AuthenticationFailed('Expired token.')

        try:
            user = model.objects.get(id=claims.get('uid'))
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token payload.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)

    def authenticate_header(self, request):
        return self.keyword
