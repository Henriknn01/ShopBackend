from django.contrib import admin
from .models import Discount, ProductCategory, Product, OrderDetails, OrderItems, User, Tag, Image, ProductList, WishList, ProductReview, BlogPost
from guardian.admin import GuardedModelAdmin
# Register your models here.


class ShopCMSAdmin(GuardedModelAdmin):
    pass

admin.site.register(Discount, ShopCMSAdmin)
admin.site.register(Tag, ShopCMSAdmin)
admin.site.register(ProductCategory, ShopCMSAdmin)
admin.site.register(Product, ShopCMSAdmin)
admin.site.register(Image, ShopCMSAdmin)
admin.site.register(ProductList, ShopCMSAdmin)
admin.site.register(BlogPost, ShopCMSAdmin)

# gray area
admin.site.register(User, ShopCMSAdmin)

# needs object level perm
admin.site.register(WishList, ShopCMSAdmin)
admin.site.register(ProductReview, ShopCMSAdmin)
admin.site.register(OrderDetails, ShopCMSAdmin)
admin.site.register(OrderItems, ShopCMSAdmin)

