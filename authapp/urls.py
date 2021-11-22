from django.urls import path

from authapp.views import register, login

app_name = 'authapp'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register')
]
