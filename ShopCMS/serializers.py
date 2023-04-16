from guardian.shortcuts import assign_perm
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

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

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        #creates discount
        discount = Discount.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_discount', group, discount)
        assign_perm('delete_discount', group, discount)
        return discount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        #creates tag
        tag = Tag.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_tag', group, tag)
        assign_perm('delete_tag', group, tag)
        return tag



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["name", "desc", "sku", "tags", "cost", "price", "quantity", "discount", "images", "category"]

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        #pops data that will be set later, and creates product
        tags_data = validated_data.pop('tags', [])
        categories_data = validated_data.pop('category', [])
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        # change products to set catagory, tags and images
        product.category.set(categories_data)
        product.tags.set(tags_data)
        product.images.set(images_data)

        # assign perms to group
        assign_perm('change_product', group, product)
        assign_perm('delete_product', group, product)
        return product


class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "products"]

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # creates catagory
        productCategory = ProductCategory.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_productcategory', group, productCategory)
        assign_perm('delete_productcategory', group, productCategory)
        return productCategory


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # creates productImage
        productImage = ProductImage.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_productimage', group, productImage)
        assign_perm('delete_productimage', group, productImage)
        return productImage



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # pops data that will be set later, and creates ProductList
        products = validated_data.pop('products', [])
        productlist = ProductList.objects.create(**validated_data)

        # change productlist to add products
        productlist.products.set(products)

        # assign perms to group
        assign_perm('change_productlist', group, productlist)
        assign_perm('delete_productlist', group, productlist)
        return productlist


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

    def create(self, validated_data):

        # get user that creates the wishlist
        owner = self.context['request'].user
        # gets user group
        group = Group.objects.get(name="user")

        # pops data that wil be set later. and creates the wishlist
        products = validated_data.pop('products', [])
        wishlist = WishList.objects.create(**validated_data)

        # change wishlist to set products
        wishlist.products.set(products)

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

        # get user that creates the productReview
        owner = self.context['request'].user
        # gets group user
        group = Group.objects.get(name="user")

        # creates review
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

        # gets owner of the orderDetail
        owner = self.context['request'].user
        # gets group support
        group = Group.objects.get(name="support")

        # creates the order
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
        # gets owner of the orderitems
        owner = self.context['request'].user
        # get support group
        group = Group.objects.get(name="support")

        # creates orderItems
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

        # gets owner of ordershipping
        owner = self.context['request'].user
        # gets group support
        group = Group.objects.get(name="support")

        # creates ordershipping
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
        # gets owner of payment details
        owner = self.context['request'].user

        # creates payment details
        paymentdetails = PaymentDetails.objects.create(**validated_data)

        # User perms
        assign_perm('view_paymentdetails', owner, paymentdetails)
        return paymentdetails
