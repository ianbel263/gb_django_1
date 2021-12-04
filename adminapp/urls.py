from django.urls import path

from adminapp.views import index, users, user_create, user_update, user_delete, categories, category_create, \
    category_update, category_delete, product_create, products, product_update, product_delete

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
    path('product_create/', product_create, name='product_create'),
    path('products/', products, name='products'),
    path('product_update/<int:pk>', product_update, name='product_update'),
    path('product_delete/<int:pk>', product_delete, name='product_delete'),
]
