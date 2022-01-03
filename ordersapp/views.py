# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm, OrderInlineFormSet
from ordersapp.models import Order, OrderItem


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    extra_context = {
        'title': 'GeekShop - все заказы'
    }

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - создание заказа'
    }
    formset = None
    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                         formset=OrderInlineFormSet, extra=0)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        return super(OrderCreateView, self).get_context_data(order_items=self.formset, **kwargs)

    def get(self, request, *args, **kwargs):
        baskets = Basket.objects.filter(user=request.user)
        if baskets:
            self.OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                                      formset=OrderInlineFormSet, extra=baskets.count())
            self.formset = self.OrderFormSet(
                initial=[{
                    'product_id': basket.product.pk,
                    'product_name': basket.product.name,
                    'quantity': basket.quantity,
                    'price': basket.total_price
                } for basket in baskets])
        else:
            self.formset = self.OrderFormSet()

        return super(OrderCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.formset = self.OrderFormSet(request.POST)
        return super(OrderCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        baskets = Basket.objects.filter(user=self.request.user)
        with transaction.atomic():
            form.instance.user = self.request.user
            if baskets:
                baskets.delete()
            self.object = form.save()
            if self.formset.is_valid():
                self.formset.instance = self.object
                self.formset.save()
            if self.object.total_price == 0:
                self.object.delete()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - редактирование заказа'
    }
    formset = None
    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                         formset=OrderInlineFormSet, extra=0)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        return super(OrderUpdateView, self).get_context_data(order_items=self.formset, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.formset = self.OrderFormSet(instance=self.object)
        for form in self.formset:
            if form.instance.pk:
                form.initial['product_id'] = form.instance.product_id
                form.initial['product_name'] = form.instance.product.name
                form.initial['price'] = form.instance.total_price
        return super(OrderUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.formset = self.OrderFormSet(request.POST, instance=self.object)
        return super(OrderUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
            if self.object.total_price == 0:
                self.object.delete()
            return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - удаление заказа'
    }


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    extra_context = {
        'title': 'GeekShop - просмотр заказа'
    }


@login_required
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))
