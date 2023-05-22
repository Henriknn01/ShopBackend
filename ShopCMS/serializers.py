from guardian.shortcuts import assign_perm
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

import ShopCMS.views
from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, Image, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, OrderShippingDetails, PaymentDetails, BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

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



class ProductDetailedSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "desc", "sku", "category", "tag", "cost", "price", "quantity", "discount",
                  "image", "created_at", "modified_at", "deleted_at"]


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


class ProductUserSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ["id", "name", "desc", "sku", "tag", "price", "quantity", "discount", "image", "category"]

class ProductCategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "desc", "image", "parent_category"]



    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="Sale")
        user = self.context['request'].user
        if not user.groups.filter(name='Sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # creates catagory
        productCategory = ProductCategory.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_productcategory', group, productCategory)
        assign_perm('delete_productcategory', group, productCategory)
        return productCategory




    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # creates Image
        CreatedImage = Image.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_image', group, CreatedImage)
        assign_perm('delete_image', group, CreatedImage)
        return CreatedImage



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


class OrderItemsSerializer(serializers.ModelSerializer):
    ordered_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItems
        fields = ['id', "ordered_product", "quantity", 'created_at', 'modified_at']

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
        fields = ["id", "full_name", "address", "city", "country", "region", "postal_code", "phone_number"]

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
        fields = ["amount", "provider", "status"]

    def create(self, validated_data):
        # gets owner of payment details
        owner = self.context['request'].user

        # creates payment details
        paymentdetails = PaymentDetails.objects.create(**validated_data)

        # User perms
        assign_perm('view_paymentdetails', owner, paymentdetails)
        return paymentdetails


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ["user", "total", "voided", "paymentDetails", "Items", "ShippingDetails", "created_at", "modified_at"]

    def get_permissions(self):
        user = self.context['request'].user
        obj = self.instance

        # Check if the user has the required permission to view the object
        if user.has_perm('ShopCMS_view_paymentDetails', obj):
            raise PermissionDenied("You do not have permission to view this product.")

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


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        # creates orderItems
        created_blog_post = BlogPost.objects.create(**validated_data)

        # Group perms
        assign_perm('edit_orderitems', group, created_blog_post)

        return created_blog_post