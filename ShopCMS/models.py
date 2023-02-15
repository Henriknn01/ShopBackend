from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase

# Create your models here.


class User(AbstractUser):
    subscribed_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.email)


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


class Tag(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)



class ProductCategory(models.Model):
    parent_category = models.ForeignKey('self', default=None, blank=True, null=True, related_name='sub_categories',
                                        on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name


class ProductInventory(models.Model): # TODO: DELETE THIS AND ADD QUANTITY DIRECTLY TO PRODUCT?
    quantity = models.PositiveIntegerField(blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"


class Product(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    sku = models.CharField(max_length=128, blank=True, null=True)
    category = models.ManyToManyField(ProductCategory)
    tags = models.ManyToManyField(Tag)
    cost = models.FloatField(default=0)
    price = models.FloatField(default=0)
    inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    src = models.CharField(max_length=512)
    alt = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductList(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WishList(ProductList):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


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


class OrderShippingDetails(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=128)


class PaymentDetails(models.Model):
    order = models.OneToOneField(OrderDetails, on_delete=models.PROTECT)
    amount = models.FloatField()
    provider = models.CharField(max_length=256, null=False, default="Unknown")
    status = models.CharField(max_length=256, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id}: {self.status}"
