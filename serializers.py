from django.conf import settings

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from .models import NonceRequest, TokenRequest
from .tokens import AccessToken


class ObtainNonceSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    class Meta:
        model = NonceRequest
        fields = (
            'phone_number',
        )


class ObtainTokenSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    nonce = serializers.CharField(required=True, allow_blank=False,
                                  allow_null=False,)
