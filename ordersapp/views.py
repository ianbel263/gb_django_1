# Create your views here.
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order
    extra_context = {
        'title': 'GeekShop - все заказы'
    }


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - создание заказа'
    }

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            baskets = Basket.objects.filter(user=self.request.user)
            if baskets:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=baskets.count())
                formset = OrderFormSet()
                for i, form in enumerate(formset.forms):
                    form.initial['product'] = baskets[i].product
                    form.initial['quantity'] = baskets[i].quantity
                    form.initial['price'] = baskets[i].total_price
                baskets.delete()
            else:
                formset = OrderFormSet()

        context['order_items'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
            if self.object.total_price == 0:
                self.object.delete()
            return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - редактирование заказа'
    }

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.total_price

        context['order_items'] = formset
        return context

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


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')
    extra_context = {
        'title': 'GeekShop - удаление заказа'
    }


class OrderDetailView(DetailView):
    model = Order
    extra_context = {
        'title': 'GeekShop - просмотр заказа'
    }


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('ordersapp:list'))
