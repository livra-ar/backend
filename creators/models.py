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

    def set_password(self, raw_password):
        """
        Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """
        Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)



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