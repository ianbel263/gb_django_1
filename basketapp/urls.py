from django.urls import path

from basketapp.views import BasketAddView, BasketUpdateView, BasketDeleteView

app_name = 'basketapp'
urlpatterns = [
    path('add/<int:product_pk>/', BasketAddView.as_view(), name='add_basket'),
    path('delete/<int:pk>/', BasketDeleteView.as_view(), name='delete_basket'),
    path('update/', BasketUpdateView.as_view(), name='update_basket')
]
