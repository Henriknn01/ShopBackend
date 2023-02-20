from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ShopCMS.views import UserViewSet, DiscountViewSet, ProductCategoryViewSet, ProductViewSet, \
    OrderDetailsViewSet, OrderItemsViewSet, PaymentDetailsViewSet, WishListViewSet

router = routers.DefaultRouter()

# Register views in the router here:
router.register('users', UserViewSet)
router.register('discounts', DiscountViewSet)
router.register('product-categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)
router.register('order-details', OrderDetailsViewSet)
router.register('order-items', OrderItemsViewSet)
router.register('payment-details', PaymentDetailsViewSet)
router.register('wishlist', WishListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
