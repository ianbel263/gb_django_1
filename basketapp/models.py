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

    def get_sum(self):
        return self.product.price * self.quantity

    def get_total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.get_sum() for basket in baskets)

    def get_total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

