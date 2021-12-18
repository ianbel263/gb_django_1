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


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

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
        today = timezone.now().date()
        birthday_date = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if data['photo_100']:
        url = data['photo_100']
        users_img_directory = 'users_img'
        filename = str(data['id'])  # + '.jpg'
        destination = os.path.join(MEDIA_ROOT, users_img_directory, filename)
        urlretrieve(url, destination)
        img_path = os.path.join(users_img_directory, filename)
        user.image = img_path

    user.save()
