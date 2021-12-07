import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, RedirectView

from basketapp.models import Basket
from mainapp.models import Product


class BasketAddView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('mainapp:detail', kwargs={'pk': self.kwargs.get('product_pk')})
        return super(BasketAddView, self).get_redirect_url(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_pk = self.kwargs.get('product_pk')
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


class BasketDeleteView(LoginRequiredMixin, DeleteView):
    model = Basket

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class BasketUpdateView(LoginRequiredMixin, View):
    def post(self, request):
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
