from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status, exceptions, generics, views

from .models import TokenRequest
from .tokens import AccessToken
from .serializers import ObtainNonceSerializer, ObtainTokenSerializer


class ObtainNonceView(generics.CreateAPIView):
    """Create a ``NonceRequest`` record"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ObtainNonceSerializer
    # TODO: apply throttling.

    def perform_create(self, serializer):
        """Pass request detail to serializer, save in ``NonceRequest`` model"""
        serializer.save(
            # TODO: Add fields like 'X_FORWARDDED', 'AGENT' and more.
            remote_addr=self.request.META.get('REMOTE_ADDR'),
        )


class ObtainTokenView(views.APIView):
    """Return access token if user provides valid nonce"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        model = get_user_model()
        try:
            user = model.objects.get(
                phone_number=validated_data['phone_number'],
                is_active=True,
            )
            valid_nonce = user.check_nonce(validated_data['nonce'])
        except model.DoesNotExist:
            user = None

        # Log token request.
        TokenRequest.objects.create(
            user=user,
            remote_addr=self.request.META.get('REMOTE_ADDR'),
            succeed=valid_nonce,
            **validated_data,
        )
        if user and valid_nonce:
            token = AccessToken(user.id).as_dict
            return Response(token, status=status.HTTP_201_CREATED)
        raise exceptions.AuthenticationFailed('Invalid username or nonce.')
