import json

from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import get_objects_for_user
from requests import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer

from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, Image, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, OrderShippingDetails, PaymentDetails, BlogPost
from ShopCMS.serializers import UserSerializer, DiscountSerializer, ProductCategorySerializer, \
    OrderDetailsSerializer, OrderItemsSerializer, PaymentDetailsSerializer, \
    TagSerializer, ImageSerializer, ProductListSerializer, WishListSerializer, \
    ProductReviewSerializer, OrderShippingDetailsSerializer, ProductUserSerializer, ProductDetailedSerializer, BlogPostSerializer

from functools import wraps
import jwt
from django.http import JsonResponse, HttpResponse
from rest_framework.filters import SearchFilter, OrderingFilter




# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'email', 'subscribed_newsletter']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_user", queryset)

    def get_serializer_class(self): #TODO fixthis make it so user can see only user name and stuff, but can see they own user account
        user = self.request.user
        if "ShopCMS.view_user" not in user.get_group_permissions():
            return UserSerializer
        elif "ShopCMS.view_product" in user.get_group_permissions():
            return UserSerializer
        else:
            return super().get_serializer_class()



class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name', 'desc', 'discount_price', 'active', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name', 'description', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'parent_category', 'name', 'desc', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']


    def perform_create(self, serializer):
        serializer.save()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name', 'category', 'sku', 'tag', 'price', 'discount', 'quantity', 'deleted_at']
    search_fields = ['=name']
    ordering_fields = ['name', 'id', 'category', 'tag', 'price']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        user = self.request.user
        if "ShopCMS.view_product" not in user.get_group_permissions():
            return ProductUserSerializer
        elif "ShopCMS.view_product" in user.get_group_permissions():
            return ProductDetailedSerializer
        else:
            return super().get_serializer_class()


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()



class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'name', 'slug', 'featured', 'category', 'image', 'products', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']


    def perform_create(self, serializer):
        serializer.save()




class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'user', 'slug', 'products', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'author', 'content', 'rating', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']


    def perform_create(self, serializer):
        serializer.save()


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'user', 'total', 'voided', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_orderdetails", queryset)


    def perform_create(self, serializer):
        serializer.save()


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'order', 'product', 'quantity', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_orderitems", queryset)

    def perform_create(self, serializer):
        serializer.save()


class OrderShippingDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderShippingDetails.objects.all()
    serializer_class = OrderShippingDetailsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'order', 'full_name', 'address', 'city', 'country', 'region', 'postal_code', 'phone_number','created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_ordershippingdetails", queryset)


    def perform_create(self, serializer):
        serializer.save()


class PaymentDetailsViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'order', 'amount', 'provider', 'status', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_paymentdetails", queryset)


    def perform_create(self, serializer):
        serializer.save()

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'author', 'banner_image', 'title', 'short_content_display', 'content', 'created_at', 'modified_at']
    search_fields = ['=id']
    ordering_fields = ['id', 'created_at']
    ordering = ['id']

    def perform_create(self, serializer):
        serializer.save()

