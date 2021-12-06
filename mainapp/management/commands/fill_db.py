import os
import subprocess

from django.core.management.base import BaseCommand

from authapp.models import User

MODELS = [
    {
        'name': 'category',
        'plural_name': 'categories'
    },
    {
        'name': 'product',
        'plural_name': 'products'
    }
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        # for model in MODELS:
        #     self.__save_data(model)
        self.__remove_db()
        self.__apply_migrations()
        for model in MODELS:
            self.__load_data(model)
        self.__add_super_user()

    @staticmethod
    def __remove_db():
        try:
            os.remove('db.sqlite3')
        except FileNotFoundError:
            print('Файл БД не найден')
        else:
            print('Файл БД удален успешно')

    @staticmethod
    def __apply_migrations():
        subprocess.call(['python3', 'manage.py', 'makemigrations'])
        subprocess.call(['python3', 'manage.py', 'migrate'])

    @staticmethod
    def __load_data(model):
        subprocess.call(['python3', 'manage.py', 'loaddata', f'fixtures/{model["plural_name"]}.json'])

    @staticmethod
    def __save_data(model):
        with open(f'./fixtures/{model["plural_name"]}.json', 'w') as f:
            subprocess.call(['python3', 'manage.py', 'dumpdata', f'mainapp.{model["name"]}'], stdout=f)

    @staticmethod
    def __add_super_user():
        User.objects.create_superuser('andrey', '1@mail.ru', '1')
