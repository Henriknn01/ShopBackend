from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ShopCMS.views import UserViewSet, DiscountViewSet, ProductCategoryViewSet, ProductViewSet, \
    OrderDetailsViewSet, OrderItemsViewSet, PaymentDetailsViewSet, WishListViewSet, TagViewSet, ProductImageViewSet, \
    ProductListViewSet, ProductReviewViewSet, OrderShippingDetailsViewSet

router = routers.DefaultRouter()

# Register views in the router here:
router.register('users', UserViewSet, basename='users')
router.register('discounts', DiscountViewSet, basename='discounts')
router.register('Tag', TagViewSet, basename='tags')
router.register('product-categories', ProductCategoryViewSet, basename='product-categories')
router.register('products', ProductViewSet, basename='products')
router.register('productsImage', ProductImageViewSet, basename='product-images')
router.register('productsList', ProductListViewSet, basename='product-lists')
router.register('wishlist', WishListViewSet, basename='wishlist')
router.register('productReview', ProductReviewViewSet, basename='product-reviews')
router.register('order-details', OrderDetailsViewSet, basename='order-details')
router.register('order-items', OrderItemsViewSet, basename='order-items')
router.register('order-shipping-detail', OrderShippingDetailsViewSet, basename='order-shipping-details')
router.register('payment-details', PaymentDetailsViewSet, basename='payment-details')

urlpatterns = [
    path('', include(router.urls)),
]
