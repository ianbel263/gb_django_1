import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def add_basket(request, product_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:detail', args=[product_pk]))

    user = request.user
    product = get_object_or_404(Product, pk=product_pk)
    baskets = Basket.objects.filter(user=user, product=product)
    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user, product=product, quantity=1)
    return JsonResponse({
        'success': True
    })


@login_required
def delete_basket(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_basket(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        basket_id = data['basketID']
        quantity = int(data['quantity'])
        basket = Basket.objects.get(id=basket_id)
        basket.quantity = quantity
        basket.save()
        return JsonResponse({
            'basketID': basket_id,
            'quantity': quantity,
            'price': basket.total_price,
            'totalPrice': basket.total_all_price,
            'totalQuantity': basket.total_quantity
        })
    else:
        return HttpResponseRedirect(reverse('index'))
