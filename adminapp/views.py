from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import UserCreateForm, UserUpdateForm, CategoryForm, ProductForm
from authapp.models import User
from adminapp.mixins import ProtectDispatchMixin, AdminDeleteMixin
from mainapp.models import Category, Product

titles = {
    'admin_index': 'Geekshop - Админ.панель',
    'admin_user': {
        'create': 'Geekshop - Админ.панель|Пользователи-добавление',
        'read': 'Geekshop - Админ.панель|Пользователи',
        'update': 'Geekshop - Админ.панель|Пользователи-обновление',
    },
    'admin_category': {
        'create': 'Geekshop - Админ.панель|Категории-добавление',
        'read': 'Geekshop - Админ.панель|Категории',
        'update': 'Geekshop - Админ.панель|Категории-обновление',
    },
    'admin_product': {
        'create': 'Geekshop - Админ.панель|Товары-добавление',
        'read': 'Geekshop - Админ.панель|Товары',
        'update': 'Geekshop - Админ.панель|Товары-обновление',
    },
}

success_messages = {
    'create': 'Данные успешно добавлены',
    'update': 'Данные успешно обновлены',
}


# Главная страница админки
class AdminTemplateView(ProtectDispatchMixin, TemplateView):
    extra_context = {'title': titles['admin_index']}
    template_name = 'adminapp/main.html'


# Отображение пользователей
class AdminUsersListView(ProtectDispatchMixin, ListView):
    model = User
    extra_context = {'title': titles['admin_user'].get('read')}
    context_object_name = 'users'
    template_name = 'adminapp/users.html'


class AdminUserCreateView(SuccessMessageMixin, ProtectDispatchMixin, CreateView):
    model = User
    form_class = UserCreateForm
    extra_context = {'title': titles['admin_user'].get('create')}
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('adminapp:users')
    success_message = success_messages['create']


class AdminUserUpdateView(SuccessMessageMixin, ProtectDispatchMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    extra_context = {'title': titles['admin_user'].get('update')}
    template_name = 'adminapp/user_update_delete.html'
    success_url = reverse_lazy('adminapp:users')
    success_message = success_messages['update']


class AdminUserDeleteView(SuccessMessageMixin, ProtectDispatchMixin, AdminDeleteMixin, DeleteView):
    model = User
    success_url = reverse_lazy('adminapp:users')


# Отображение категорий товаров
class AdminCategoriesListView(ProtectDispatchMixin, ListView):
    model = Category
    context_object_name = 'categories'
    extra_context = {'title': titles['admin_category'].get('read')}
    template_name = 'adminapp/categories.html'


class AdminCategoryCreateView(SuccessMessageMixin, ProtectDispatchMixin, CreateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'title': titles['admin_category'].get('create')}
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('adminapp:categories')
    success_message = success_messages['create']


class AdminCategoryUpdateView(SuccessMessageMixin, ProtectDispatchMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    extra_context = {'title': titles['admin_category'].get('update')}
    template_name = 'adminapp/category_update_delete.html'
    success_url = reverse_lazy('adminapp:categories')
    success_message = success_messages['update']


class AdminCategoryDeleteView(SuccessMessageMixin, ProtectDispatchMixin, AdminDeleteMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('adminapp:categories')


# Отображение товаров
class AdminProductsListView(ProtectDispatchMixin, ListView):
    model = Product
    context_object_name = 'products'
    extra_context = {'title': titles['admin_product'].get('read')}
    template_name = 'adminapp/products.html'

    def get_queryset(self):
        return Product.objects.select_related()


class AdminProductCreateView(SuccessMessageMixin, ProtectDispatchMixin, CreateView):
    model = Product
    form_class = ProductForm
    extra_context = {'title': titles['admin_product'].get('create')}
    template_name = 'adminapp/product_create.html'
    success_url = reverse_lazy('adminapp:products')
    success_message = success_messages['create']


class AdminProductUpdateView(SuccessMessageMixin, ProtectDispatchMixin, UpdateView):
    model = Product
    form_class = ProductForm
    extra_context = {'title': titles['admin_product'].get('update')}
    template_name = 'adminapp/product_update_delete.html'
    success_url = reverse_lazy('adminapp:products')
    success_message = success_messages['update']


class AdminProductDeleteView(SuccessMessageMixin, ProtectDispatchMixin, AdminDeleteMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('adminapp:products')
