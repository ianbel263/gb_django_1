from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def get_expire_time():
    return now() + timedelta(hours=48)


class User(AbstractUser):
    image = models.ImageField(upload_to='users_img', blank=True)
    age = models.PositiveIntegerField(default=18)
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': _("A user with that email already exists."),
    }, )

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires_at = models.DateTimeField(default=get_expire_time, blank=True, null=True)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires_at
