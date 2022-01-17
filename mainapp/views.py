from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView

from .models import Product, Category


class IndexTemplateView(TemplateView):
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'GeekShop'}


class ProductsListView(ListView):
    model = Product
    queryset = Product.objects.filter(is_active=True, quantity__gt=0)
    category_pk = None
    template_name = 'mainapp/products.html'
    context_object_name = 'products'
    paginate_by = 6
    page_kwarg = 'page_number'

    def get_context_data(self, **kwargs):
        self.category_pk = self.kwargs.get('category_pk')
        title = 'GeekShop - Каталог'
        if self.category_pk:
            self.queryset = Product.objects.filter(is_active=True, category=self.category_pk, quantity__gt=0)
            title = f'GeekShop - Каталог|{Category.objects.get(pk=self.category_pk).name}'

        context = super(ProductsListView, self).get_context_data(object_list=self.queryset, **kwargs)
        if self.paginate_by:
            current_page = context['page_obj'].number
            page_range = context['paginator'].get_elided_page_range(current_page)
        else:
            current_page = None
            page_range = None

        context.update({
            'title': title,
            'current_category': self.category_pk,
            'categories': Category.objects.filter(is_active=True),
            'page_range': page_range
        })
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        self.extra_context.update({'title': f'GeekShop - {self.object.name}'})
        return super(ProductDetailView, self).get_context_data(**kwargs)
