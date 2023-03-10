from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ShopCMS.views import UserViewSet, DiscountViewSet, ProductCategoryViewSet, ProductViewSet, \
    OrderDetailsViewSet, OrderItemsViewSet, PaymentDetailsViewSet, WishListViewSet, TagViewSet, ProductImageViewSet, \
    ProductListViewSet, ProductReviewViewSet, OrderShippingDetailsViewSet

router = routers.DefaultRouter()

# Register views in the router here:
router.register('user', UserViewSet, basename='user')
router.register('discount', DiscountViewSet, basename='discount')
router.register('tag', TagViewSet, basename='tag')
router.register('productcategory', ProductCategoryViewSet, basename='product-category')
router.register('product', ProductViewSet, basename='product')
router.register('productsImage', ProductImageViewSet, basename='product-image')
router.register('productlist', ProductListViewSet, basename='product-list')
router.register('wishlist', WishListViewSet, basename='wishlist')
router.register('productReview', ProductReviewViewSet, basename='product-review')
router.register('order', OrderDetailsViewSet, basename='order-detail')
router.register('order-item', OrderItemsViewSet, basename='order-item')
router.register('order-shipping', OrderShippingDetailsViewSet, basename='order-shipping-detail')
router.register('payment', PaymentDetailsViewSet, basename='payment-detail')

urlpatterns = [
    path('', include(router.urls)),
]
