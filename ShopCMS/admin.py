from django.contrib import admin
from .models import Discount, ProductCategory, ProductInventory, Product, OrderDetails, OrderItems, PaymentDetails, \
    OrderShippingDetails
# Register your models here.

admin.site.register(Discount)
admin.site.register(ProductCategory)
admin.site.register(ProductInventory)
admin.site.register(Product)
admin.site.register(OrderDetails)
admin.site.register(OrderItems)
admin.site.register(PaymentDetails)
admin.site.register(OrderShippingDetails)
