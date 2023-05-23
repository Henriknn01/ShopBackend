from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ShopCMS.views import UserViewSet, DiscountViewSet, ProductCategoryViewSet, ProductViewSet, \
    OrderDetailsViewSet, OrderItemsViewSet, PaymentDetailsViewSet, WishListViewSet, TagViewSet, ImageViewSet, \
    ProductListViewSet, ProductReviewViewSet, OrderShippingDetailsViewSet, BlogPostViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
router = routers.DefaultRouter()

# Register views in the router here:
router.register('user', UserViewSet, basename='user')
router.register('discount', DiscountViewSet, basename='discount')
router.register('tag', TagViewSet, basename='tag')
router.register('productcategory', ProductCategoryViewSet, basename='product-category')
router.register('product', ProductViewSet, basename='product')
router.register('Image', ImageViewSet, basename='image')
router.register('blogpost', BlogPostViewSet, basename='blogpost')
router.register('productlist', ProductListViewSet, basename='product-list')
router.register('wishlist', WishListViewSet, basename='wishlist')
router.register('productReview', ProductReviewViewSet, basename='product-review')
router.register('order', OrderDetailsViewSet, basename='order-detail')
router.register('order-item', OrderItemsViewSet, basename='order-item')
router.register('order-shipping', OrderShippingDetailsViewSet, basename='order-shipping-detail')
router.register('payment', PaymentDetailsViewSet, basename='payment-detail')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
