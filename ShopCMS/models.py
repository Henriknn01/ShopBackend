import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase


class User(AbstractUser):
    subscribed_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    """
    Model representing a user with a subscribed_newsletter field.
    """


class Discount(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    discount_price = models.FloatField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.id}"

    """
    Model representing a discount with a name, description, discount price, active status, and timestamp fields.
    """


class Tag(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.id}"


# this needs no perms, everybody even anon should be able to see categorys
class ProductCategory(models.Model):
    parent_category = models.ForeignKey('self', default=None, blank=True, null=True, related_name='sub_categories',
                                        on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.id}"


# this needs only perms on cost where we cant share what we buy them for
class Product(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    desc = models.TextField(max_length=5000)
    sku = models.CharField(max_length=128, blank=True, null=True)
    category = models.ManyToManyField(ProductCategory, related_name="products", null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    cost = models.FloatField(default=0)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(blank=False, default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.id}"


# this needs no perms to view
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    src = models.CharField(max_length=512)
    alt = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}-{self.src}-{self.id}"


# this needs no perms to view
class ProductList(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# this needs per object as only the user who created can edit, everybody can view
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=256, default=uuid.uuid4)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ('view',)

    def __str__(self):
        return f"{self.slug}"


# this needs per object
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, null=False, blank=False)
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}-{self.author.id}"


# this needs per object
class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.FloatField()
    voided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"


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


# this needs per object
class PaymentDetails(models.Model):
    order = models.OneToOneField(OrderDetails, on_delete=models.PROTECT)
    amount = models.FloatField()
    provider = models.CharField(max_length=256, null=False, default="Unknown")
    status = models.CharField(max_length=256, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id}: {self.status}"
