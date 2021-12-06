from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import Category, Product


# Create your views here.
def index(request):
    title = 'GeekShop'
    context = {
        'title': title
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_pk):
    title = 'GeekShop - Каталог'
    if category_pk == 0:
        category = 'Все товары'
        selected_products = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(Category, pk=category_pk)
        selected_products = Product.objects.filter(category=category_pk, is_active=True)

    context = {
        'title': title,
        'category': category,
        'categories': Category.objects.filter(is_active=True),
        'products': selected_products
    }
    return render(request, 'mainapp/products.html', context)


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'GeekShop - {product.name}'
    context = {
        'title': title,
        'product': product
    }
    return render(request, 'mainapp/detail.html', context)

