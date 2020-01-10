# Generated by Django 2.2.9 on 2020-01-10 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NonceRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('remote_addr', models.GenericIPAddressField(editable=False)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(editable=False, max_length=128, region=None, verbose_name='phone number')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TokenRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('remote_addr', models.GenericIPAddressField(editable=False, verbose_name='ip address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(editable=False, max_length=128, region=None, verbose_name='phone number')),
                ('nonce', models.CharField(editable=False, max_length=8, verbose_name='nonce')),
                ('succeed', models.BooleanField(editable=False, verbose_name='succeed')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='token_request', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
