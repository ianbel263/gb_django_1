# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def add_basket(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
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
def delete_basket(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
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
            'price': basket.get_sum(),
            'totalPrice': basket.get_total_sum(),
            'totalQuantity': basket.get_total_quantity()
        })
