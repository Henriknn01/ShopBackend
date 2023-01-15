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
        fields = '__all__'


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductInventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductInventory
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class PaymentDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
