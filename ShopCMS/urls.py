from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ShopCMS.views import UserViewSet, DiscountViewSet, ProductCategoryViewSet, ProductInventoryViewSet, ProductViewSet, \
    OrderDetailsViewSet, OrderItemsViewSet, PaymentDetailsViewSet

router = routers.DefaultRouter()

# Register views in the router here:
router.register('users', UserViewSet)
router.register('discounts', DiscountViewSet)
router.register('product-categories', ProductCategoryViewSet)
router.register('product-inventories', ProductInventoryViewSet)
router.register('products', ProductViewSet)
router.register('order-details', OrderDetailsViewSet)
router.register('order-items', OrderItemsViewSet)
router.register('payment-details', PaymentDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
