from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, ListView, DetailView

from .models import Product, Category


class IndexTemplateView(TemplateView):
    template_name = 'mainapp/index.html'
    extra_context = {'title': 'GeekShop'}


class ProductsListView(ListView):
    queryset = Product.objects.filter(is_active=True)
    template_name = 'mainapp/products.html'
    extra_context = {'title': 'GeekShop - Каталог'}
    context_object_name = 'products'
    paginate_by = 3
    page_kwarg = 'page_number'

    def get_context_data(self, **kwargs):
        self.extra_context.update({'categories': Category.objects.filter(is_active=True)})
        return super(ProductsListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        category_pk = self.kwargs.get('category_pk')
        return Product.objects.filter(is_active=True, category=category_pk) if category_pk else self.queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        self.extra_context.update({'title': f'GeekShop - {self.object.name}'})
        return super(ProductDetailView, self).get_context_data(**kwargs)
