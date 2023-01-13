from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Discount(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    discount_price = models.FloatField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name


class ProductInventory(models.Model):
    quantity = models.PositiveIntegerField(blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"


class Product(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    sku = models.CharField(max_length=128)
    category = models.ManyToManyField(ProductCategory)
    inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE)
    cost = models.FloatField()
    price = models.FloatField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name


class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.FloatField()
    voided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class OrderItems(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class PaymentDetails(models.Model):
    order = models.OneToOneField(OrderDetails, on_delete=models.PROTECT)
    amount = models.FloatField()
    provider = models.CharField(max_length=256, null=False, default="Unknown")
    status = models.CharField(max_length=256, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id}: {self.status}"

