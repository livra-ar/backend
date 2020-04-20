from django.db import models
from django.utils import timezone
import datetime
import binascii
import os
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import _user_has_perm,  _user_has_module_perms#,_user_get_all_permissions,

import mongoengine
from mongoengine import fields, Document, ImproperlyConfigured

# Create your models here.
class Creator(Document):    
    email = fields.EmailField(unique=True)
    is_publisher = fields.BooleanField(default=True)
    is_confirmed = fields.BooleanField(default=False)
    name = fields.StringField(required=True)
    password = fields.StringField(
        max_length=128,
        verbose_name=_('password'),required=True)
    
    def is_authenticated(self):
        return True

class Token(Document):
    """
    This is a mongoengine adaptation of DRF's default Token.
    The default authorization token model.
    """
    key = fields.StringField(required=True)
    user = fields.ReferenceField(Creator, reverse_delete_rule=mongoengine.CASCADE)
    created = fields.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
