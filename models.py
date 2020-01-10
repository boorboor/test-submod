from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from gardeshpay.models_abstract import BaseModel, TimeStamped
from .tokens import AccessToken


class NonceRequest(BaseModel, TimeStamped):
    """Log records of ``NonceRequestview``."""
    remote_addr = models.GenericIPAddressField(editable=False)
    phone_number = PhoneNumberField(_('phone number'), editable=False)

    def save(self, *args, **kwargs):
        """Put a nonce in cache and send it to user by sms."""
        model = get_user_model()
        try:
            user = model.objects.get(phone_number=self.phone_number)
            user.make_nonce()
        except model.DoesNotExist:
            user = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + self.remote_addr +  str(self.phone_number)


class TokenRequest(BaseModel, TimeStamped):
    """Log records of ``TokenRequestView``."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='token_request',
                                    on_delete=models.PROTECT,
                                    null=True, blank=True, editable=False)
    remote_addr = models.GenericIPAddressField(_('ip address'),editable=False)
    phone_number = PhoneNumberField(_('phone number'), editable=False)
    nonce = models.CharField(_('nonce'), max_length=8, editable=False)
    succeed = models.BooleanField(_('succeed'), editable=False)
