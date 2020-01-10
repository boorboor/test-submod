from datetime import datetime, timedelta

import jwt

from django.conf import settings


def is_valid(token,
             issuer=settings.TOKEN_ISSUER,
             algorithms=['HS256']):
    """Validate token against config or passed kwargs"""

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        issuser=issuer,
        algorithms=algorithms,
    )


class AccessToken:
    """Implements basics for token objects"""
    def __init__(self, uid):
        """Initialize token claims"""
        self.uid = str(uid)
        self.sub = 'access'
        self.iat = datetime.utcnow()
        self.nbf = datetime.utcnow()
        iss=settings.TOKEN_ISSUER
        self.exp = datetime.utcnow() + timedelta(
            seconds=settings.ACCESS_TOKEN_LIFTTIME)
        self._token = None

    @property
    def claims(self):
        """Returns all token claims"""
        claims = self.__dict__.copy()
        claims.pop('_token')
        return claims

    @property
    def token(self):
        """Returns token from object"""
        if self._token:
            return self._token
        self._token = jwt.encode(self.claims, settings.SECRET_KEY, algorithm='HS256')
        return self._token

    @property
    def as_dict(self):
        """Represents token in dict format"""
        return {'token': self.token}
