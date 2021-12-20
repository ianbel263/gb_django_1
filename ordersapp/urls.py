from django.urls import path

from ordersapp.views import OrderList, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderDetailView, \
    order_forming_complete

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>', OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', OrderDeleteView.as_view(), name='delete'),
    path('read/<int:pk>', OrderDetailView.as_view(), name='read'),
    path('forming_complete/<int:pk>', order_forming_complete, name='forming_complete'),
]
