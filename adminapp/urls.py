from django.urls import path

from adminapp.views import AdminTemplateView, \
    AdminUsersListView, AdminUserCreateView, AdminUserUpdateView, AdminUserDeleteView, \
    AdminCategoriesListView, AdminCategoryCreateView, AdminCategoryUpdateView, AdminCategoryDeleteView, \
    AdminProductCreateView, AdminProductsListView, AdminProductUpdateView, AdminProductDeleteView

app_name = 'adminapp'

urlpatterns = [
    path('', AdminTemplateView.as_view(), name='index'),
    path('user_create/', AdminUserCreateView.as_view(), name='user_create'),
    path('users/', AdminUsersListView.as_view(), name='users'),
    path('user_update/<int:pk>', AdminUserUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:pk>', AdminUserDeleteView.as_view(), name='user_delete'),
    path('category_create/', AdminCategoryCreateView.as_view(), name='category_create'),
    path('categories/', AdminCategoriesListView.as_view(), name='categories'),
    path('category_update/<int:pk>', AdminCategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', AdminCategoryDeleteView.as_view(), name='category_delete'),
    path('product_create/', AdminProductCreateView.as_view(), name='product_create'),
    path('products/', AdminProductsListView.as_view(), name='products'),
    path('product_update/<int:pk>', AdminProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>', AdminProductDeleteView.as_view(), name='product_delete'),
]
