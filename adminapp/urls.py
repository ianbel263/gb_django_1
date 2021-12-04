from django.urls import path

from adminapp.views import index, users, user_create, user_update, user_delete, categories, category_create, \
    category_update, category_delete

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('user_create/', user_create, name='user_create'),
    path('users/', users, name='users'),
    path('user_update/<int:pk>', user_update, name='user_update'),
    path('user_delete/<int:pk>', user_delete, name='user_delete'),
    path('category_create/', category_create, name='category_create'),
    path('categories/', categories, name='categories'),
    path('category_update/<int:pk>', category_update, name='category_update'),
    path('category_delete/<int:pk>', category_delete, name='category_delete'),
]
