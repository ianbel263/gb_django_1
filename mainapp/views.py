from django.shortcuts import render, get_object_or_404

from .models import Category, Product


# Create your views here.
def index(request):
    title = 'GeekShop'
    context = {
        'title': title
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    title = 'GeekShop - Каталог'
    context = {
        'title': title,
        'categories': Category.objects.all(),
        'products': Product.objects.all()
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

