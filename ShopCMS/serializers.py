from guardian.shortcuts import assign_perm
from rest_framework import serializers

import ShopCMS.views
from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, ProductImage, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, OrderShippingDetails, PaymentDetails


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'user_type', 'subscribed_newsletter']


class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'


class WishListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        products = validated_data.pop('products', [])  # Remove 'products' from validated data
        wishlist = WishList.objects.create(**validated_data)
        wishlist.products.set(products)  # Use set() to set the many-to-many relationship
        assign_perm('change_wishlist', owner, wishlist)
        assign_perm('delete_wishlist', owner, wishlist)
        assign_perm('view_wishlist', owner, wishlist)
        return wishlist


class ProductReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        productReview = ProductReview.objects.create(**validated_data)
        assign_perm('change_productreview', owner, productReview)
        assign_perm('delete_productreview', owner, productReview)
        assign_perm('view_productreview', owner, productReview)
        return productReview


class OrderDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrderShippingDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderShippingDetails
        fields = '__all__'


class PaymentDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
