import os
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse
from urllib.request import urlretrieve

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile
from geekshop.settings import MEDIA_ROOT


def save_avatar(url, user):
    users_img_directory = 'users_img'
    filename = f'{user.pk}.jpg'
    img_path = os.path.join(users_img_directory, filename)
    destination = os.path.join(MEDIA_ROOT, users_img_directory, filename)
    if not os.path.exists(destination):
        urlretrieve(url, destination)
    return img_path


def get_age(user, birthday_date):
    today = timezone.now().date()

    age = today.year - birthday_date.year - (
            (today.month, today.day) < (birthday_date.month, birthday_date.day))
    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    return age


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_100')),
                                                    access_token=response['access_token'],
                                                    v='5.131')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

        if data['about']:
            user.userprofile.about = data['about']

        if data['bdate']:
            birthday_date = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            user.age = get_age(user, birthday_date)

        if data['photo_100']:
            url = data['photo_100']
            user.image = save_avatar(url, user)

        user.save()

    elif backend.name == 'facebook':
        api_url = urlunparse(('https',
                              'graph.facebook.com',
                              '/me',
                              None,
                              urlencode(
                                  OrderedDict(fields=','.join(('id', 'birthday', 'gender', 'picture{url}')),
                                              access_token=response['access_token'],
                                              v='12.0')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()

        if data['gender']:
            user.userprofile.gender = UserProfile.MALE if data['gender'] == 'male' else UserProfile.FEMALE

        if data['birthday']:
            birthday_date = datetime.strptime(data['birthday'], '%m/%d/%Y').date()
            user.age = get_age(user, birthday_date)

        if data['picture']['data']['url']:
            url = data['picture']['data']['url']
            user.image = save_avatar(url, user)

        user.save()
