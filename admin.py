from django.contrib import admin

from .models import NonceRequest, TokenRequest


admin.site.register(NonceRequest)
admin.site.register(TokenRequest)
