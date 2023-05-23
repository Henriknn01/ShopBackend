import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase
from django.utils.translation import gettext_lazy as _

from ShopCMS.managers import UserAccountManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    subscribed_newsletter = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    def __str__(self):
        return f"{self.email}"

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
class Image(models.Model):
    src = models.CharField(max_length=512)
    alt = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.src}-{self.id}"

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
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
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
    category = models.ManyToManyField(ProductCategory, related_name="products", blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    cost = models.FloatField(default=0)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(blank=False, default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    image = models.ManyToManyField(Image, related_name="images", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.id}"


# this needs no perms to view



# this needs no perms to view
class ProductList(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    featured = models.BooleanField(default=False, null=True)
    category = models.ManyToManyField(ProductCategory, related_name="Listcategory", blank=True)
    image = models.ManyToManyField(Image, related_name="ListImages", blank=True)
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

class OrderItems(models.Model):
    ordered_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="ordered_product")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class OrderShippingDetails(models.Model):
    full_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=128)



# this needs per object
class PaymentDetails(models.Model):
    amount = models.FloatField(default=0)
    provider = models.CharField(max_length=256, null=False, default="Unknown")
    status = models.CharField(max_length=256, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.status}"


# this needs per object
class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.FloatField()
    voided = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    paymentDetails = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE, related_name='paymentDetails')
    Items = models.ManyToManyField(OrderItems, related_name="items")
    ShippingDetails = models.ForeignKey(OrderShippingDetails, on_delete=models.CASCADE, related_name="shipping")

    def __str__(self):
        return f"{self.id}"



#  https://www.tiny.cloud/
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)
    short_content_display = models.TextField()
    content = models.TextField(max_length=1024, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
