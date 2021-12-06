from django.db import models

# Create your models here.
from authapp.models import User
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина пользователя {self.user} - товар: {self.product}'

    def _get_user_baskets(self):
        return Basket.objects.filter(user=self.user)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def total_all_price(self):
        baskets = self._get_user_baskets()
        return sum(basket.total_price for basket in baskets)

    @property
    def total_quantity(self):
        baskets = self._get_user_baskets()
        return sum(basket.quantity for basket in baskets)

