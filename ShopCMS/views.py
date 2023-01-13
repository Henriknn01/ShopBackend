from django.contrib.auth.models import User
from rest_framework import viewsets
from ShopCMS.models import Discount, ProductCategory, ProductInventory, OrderDetails, OrderItems, PaymentDetails, \
    Product
from ShopCMS.serializers import UserSerializer, DiscountSerializer, ProductCategorySerializer, \
    ProductInventorySerializer, OrderDetailsSerializer, OrderItemsSerializer, PaymentDetailsSerializer, \
    ProductSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer


class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer


class PaymentDetailsViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer
