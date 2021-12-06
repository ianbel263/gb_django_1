from django.urls import path

from mainapp.views import products, detail

app_name = 'mainapp'
urlpatterns = [
    path('<int:category_pk>', products, name='products'),
    path('<int:pk>/', detail, name='detail'),
]
