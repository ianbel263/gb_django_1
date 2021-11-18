from django.shortcuts import render

from .models import Category, Product


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'products.html', context)
