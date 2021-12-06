from django.urls import path

from mainapp.views import ProductsListView, ProductDetailView

app_name = 'mainapp'
urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('category/<int:pk>', ProductsListView.as_view(), name='category'),
]
