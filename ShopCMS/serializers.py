from django.contrib.auth.models import User
from rest_framework import serializers

from ShopCMS.models import Discount, ProductCategory, ProductInventory, Product, OrderDetails, OrderItems, \
    PaymentDetails


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory


class ProductInventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductInventory


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product


class OrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetails


class OrderItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItems


class PaymentDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentDetails
