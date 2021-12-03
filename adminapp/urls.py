from django.urls import path

from adminapp.views import index, users, user_create, user_update, user_delete

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('user_create/', user_create, name='user_create'),
    path('users/', users, name='users'),
    path('user_update/<int:pk>', user_update, name='user_update'),
    path('user_delete/<int:pk>', user_delete, name='user_delete'),
]
