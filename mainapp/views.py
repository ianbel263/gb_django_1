from django.shortcuts import render

from .models import Category, Product


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'mainapp/products.html', context)


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'title': f'GeekShop - {product.name}',
        'product': product
    }
    return render(request, 'mainapp/detail.html', context)

