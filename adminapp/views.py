from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse

from adminapp.forms import UserCreateForm, UserUpdateForm, CategoryForm, ProductForm
from authapp.models import User
from mainapp.models import Category, Product


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    return render(request, 'adminapp/main.html')


# Контроллеры работы с пользователями
@user_passes_test(lambda user: user.is_superuser)
def users(request):
    title = 'Geekshop - Пользователи'
    all_users = User.objects.all()
    context = {
        'title': title,
        'users': all_users
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_create(request):
    title = 'Geekshop - Создание пользователя'
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь добавлен')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = UserCreateForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/user_create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(User, pk=pk)
    title = f'Geekshop - Редактирование пользователя - "{current_user.username}"'
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, files=request.FILES, instance=current_user)
        if form.is_valid():
            if form.changed_data:
                form.save()
                messages.success(request, f'Пользователь "{current_user.username}" обновлен')
            else:
                messages.success(request, 'Вы ничего не изменили')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = UserUpdateForm(instance=current_user)
    context = {
        'title': title,
        'form': form,
        'user': current_user
    }
    return render(request, 'adminapp/user_update_delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, pk):
    if request.method == 'POST':
        current_user = get_object_or_404(User, pk=pk)
        current_user.is_active = False
        current_user.save()
        messages.success(request, 'Пользователь успешно удален')
    return HttpResponseRedirect(reverse('adminapp:users'))


# Контроллеры работы с категориями товаров
@user_passes_test(lambda user: user.is_superuser)
def categories(request):
    title = 'Geekshop - Категории товаров'
    all_categories = Category.objects.all()
    context = {
        'title': title,
        'categories': all_categories
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_create(request):
    title = 'Geekshop - Создание категории товаров'
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория добавлена')
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = CategoryForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/category_create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(Category, pk=pk)
    title = f'Geekshop - Редактирование категории товаров - "{current_category.name}"'
    if request.method == 'POST':
        form = CategoryForm(data=request.POST, instance=current_category)
        if form.is_valid():
            if form.changed_data:
                form.save()
                messages.success(request, f'Категория "{current_category.name}" обновлена')
            else:
                messages.success(request, 'Вы ничего не изменили')
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = CategoryForm(instance=current_category)
    context = {
        'title': title,
        'form': form,
        'category': current_category
    }
    return render(request, 'adminapp/category_update_delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_delete(request, pk):
    if request.method == 'POST':
        current_category = get_object_or_404(Category, pk=pk)
        current_category.is_active = False
        current_category.save()
        messages.success(request, 'Категория успешно удалена')
    return HttpResponseRedirect(reverse('adminapp:categories'))


# Контроллеры работы с товарами
@user_passes_test(lambda user: user.is_superuser)
def products(request):
    title = 'Geekshop - Товары'
    all_products = Product.objects.all()
    context = {
        'title': title,
        'products': all_products
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_create(request):
    title = 'Geekshop - Создание товара'
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар добавлен')
            return HttpResponseRedirect(reverse('adminapp:products'))
    else:
        form = ProductForm()
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_update(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    title = f'Geekshop - Редактирование товара - "{current_product.name}"'
    if request.method == 'POST':
        form = ProductForm(data=request.POST, instance=current_product, files=request.FILES)
        if form.is_valid():
            if form.changed_data:
                form.save()
                messages.success(request, f'Товар "{current_product.name}" обновлен')
            else:
                messages.success(request, 'Вы ничего не изменили')
            return HttpResponseRedirect(reverse('adminapp:products'))
    else:
        form = ProductForm(instance=current_product)
    context = {
        'title': title,
        'form': form,
        'product': current_product
    }
    return render(request, 'adminapp/product_update_delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, pk):
    if request.method == 'POST':
        current_product = get_object_or_404(Category, pk=pk)
        current_product.is_active = False
        current_product.save()
        messages.success(request, 'Товар успешно удален')
    return HttpResponseRedirect(reverse('adminapp:products'))
