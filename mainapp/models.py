from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    desc = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_img', blank=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} | {self.category}'
