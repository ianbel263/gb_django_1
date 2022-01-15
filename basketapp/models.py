from django.db import models
from django.utils.functional import cached_property

from authapp.models import User
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина пользователя {self.user} - товар: {self.product}'

    def _get_user_baskets(self):
        return Basket.objects.filter(user=self.user).select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete(*args, **kwargs)

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
