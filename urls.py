from django.urls import path

from . import views


urlpatterns = [
    path('nonce/', views.ObtainNonceView().as_view(), name='nonce'),
    path('token/', views.ObtainTokenView().as_view(), name='token'),
]
