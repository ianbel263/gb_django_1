from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    ENGLISH = 'en'
    RUSSIAN = 'ru'

    LANGUAGE_CHOICES = (
        (ENGLISH, 'english'),
        (RUSSIAN, 'русский')
    )

    user = models.OneToOneField(User, unique=True, null=False, on_delete=models.CASCADE, db_index=True)
    gender = models.CharField(verbose_name='пол', max_length=1, blank=True, choices=GENDER_CHOICES)
    about = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    language = models.CharField(verbose_name='язык', max_length=2, blank=True, choices=LANGUAGE_CHOICES,
                                default=RUSSIAN)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
