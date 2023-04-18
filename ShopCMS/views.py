from requests import Response
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer

from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, Image, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, OrderShippingDetails, PaymentDetails, BlogPost
from ShopCMS.serializers import UserSerializer, DiscountSerializer, ProductCategorySerializer, \
    OrderDetailsSerializer, OrderItemsSerializer, PaymentDetailsSerializer, \
    ProductSerializer, TagSerializer, ImageSerializer, ProductListSerializer, WishListSerializer, \
    ProductReviewSerializer, OrderShippingDetailsSerializer, BlogPostSerializer
from functools import wraps
import jwt
from django.http import JsonResponse, HttpResponse




# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]





class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def perform_create(self, serializer):
        serializer.save()



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def perform_create(self, serializer):
        serializer.save()



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save()


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save()



class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer

    def perform_create(self, serializer):
        serializer.save()



class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


    def perform_create(self, serializer):
        serializer.save()


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


    def perform_create(self, serializer):
        serializer.save()


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()


class OrderShippingDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderShippingDetails.objects.all()
    serializer_class = OrderShippingDetailsSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()


class PaymentDetailsViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save()

