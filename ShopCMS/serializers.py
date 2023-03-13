from guardian.shortcuts import assign_perm
from rest_framework import serializers
from django.contrib.auth.models import Group

import ShopCMS.views
from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, ProductImage, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, OrderShippingDetails, PaymentDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'subscribed_newsletter']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        discount = Discount.objects.create(**validated_data)
        assign_perm('change_discount', group, discount)
        assign_perm('delete_discount', group, discount)
        return discount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        tag = Tag.objects.create(**validated_data)
        assign_perm('change_tag', group, tag)
        assign_perm('delete_tag', group, tag)
        return tag


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        productCategory = ProductCategory.objects.create(**validated_data)
        assign_perm('change_productcategory', group, productCategory)
        assign_perm('delete_productcategory', group, productCategory)
        return productCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        product = Product.objects.create(**validated_data)
        assign_perm('change_product', group, product)
        assign_perm('delete_product', group, product)
        return product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        productImage = ProductImage.objects.create(**validated_data)
        assign_perm('change_productimage', group, productImage)
        assign_perm('delete_productimage', group, productImage)
        return productImage


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="sale")
        products = validated_data.pop('products', [])  # Remove 'products' from validated data
        productlist = ProductList.objects.create(**validated_data)
        productlist.products.set(products)  # Use set() to set the many-to-many relationship
        assign_perm('change_productlist', group, productlist)
        assign_perm('delete_productlist', group, productlist)
        return productlist


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        group = Group.objects.get(name="user")
        products = validated_data.pop('products', [])  # Remove 'products' from validated data
        wishlist = WishList.objects.create(**validated_data)
        wishlist.products.set(products)  # Use set() to set the many-to-many relationship
        # User perms
        assign_perm('change_wishlist', owner, wishlist)
        assign_perm('delete_wishlist', owner, wishlist)
        # Group perms
        assign_perm('view_wishlist', group, wishlist)
        return wishlist


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        group = Group.objects.get(name="user")
        productReview = ProductReview.objects.create(**validated_data)
        # User perms
        assign_perm('change_productreview', owner, productReview)
        assign_perm('delete_productreview', owner, productReview)
        # Group perms
        assign_perm('view_productreview', group, productReview)
        return productReview


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="support")
        owner = self.context['request'].user
        orderDetail = OrderDetails.objects.create(**validated_data)
        # User perms
        assign_perm('view_orderdetails', owner, orderDetail)
        # Group perms
        assign_perm('view_orderdetails', group, orderDetail)
        return orderDetail


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="support")
        owner = self.context['request'].user
        orderitems = OrderItems.objects.create(**validated_data)

        # User perms
        assign_perm('view_orderitems', owner, orderitems)

        # Group perms
        assign_perm('view_orderitems', group, orderitems)

        return orderitems


class OrderShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderShippingDetails
        fields = '__all__'

    def create(self, validated_data):
        group = Group.objects.get(name="support")
        owner = self.context['request'].user
        ordershippingdetails = OrderShippingDetails.objects.create(**validated_data)
        # User perms
        assign_perm('view_ordershippingdetails', owner, ordershippingdetails)
        # Group perms
        assign_perm('view_ordershippingdetails', group, ordershippingdetails)
        return ordershippingdetails

class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        paymentdetails = PaymentDetails.objects.create(**validated_data)
        # User perms
        assign_perm('view_paymentdetails', owner, paymentdetails)
        return paymentdetails
