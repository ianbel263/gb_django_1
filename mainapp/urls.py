from django.urls import path

from mainapp.views import ProductsListView, ProductDetailView

app_name = 'mainapp'
urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('category/<int:category_pk>', ProductsListView.as_view(), name='category'),
    path('page/<int:page_number>', ProductsListView.as_view(), name='page'),
    path('category/<int:category_pk>/page/<int:page_number>', ProductsListView.as_view(), name='category_by_page'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
