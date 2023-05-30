from guardian.shortcuts import assign_perm
from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied

import ShopCMS.views
from ShopCMS.models import User, Discount, Tag, ProductCategory, Product, Image, ProductList, \
    WishList, ProductReview, OrderDetails, OrderItems, BlogPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "subscribed_newsletter"]


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
            raise PermissionDenied("You don't have permission to create a Discount.")

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
        read_only_fields = ['id', 'created_at', 'modified_at', 'deleted_at']


    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a Tag.")

        #creates tag
        tag = Tag.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_tag', group, tag)
        assign_perm('delete_tag', group, tag)
        return tag



class ProductDetailedSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True, write_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "desc", "sku", "category", "tag", "cost", "price", "quantity", "discount",
                  "image", "created_at", "modified_at", "deleted_at"]
        read_only_fields = ['id', 'created_at', 'modified_at', 'deleted_at']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Replace the images field with serialized images data
        representation['image'] = ImageSerializer(instance.image.all(), many=True).data
        return representation

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a product.")

        #pops data that will be set later, and creates product
        tags_data = validated_data.pop('tag', [])
        categories_data = validated_data.pop('category', [])
        images_data = validated_data.pop('image', [])
        product = Product.objects.create(**validated_data)

        # change products to set catagory, tags and images
        product.category.set(categories_data)
        product.tag.set(tags_data)
        product.image.set(images_data)

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
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), write_only=True)

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "desc", "image", "parent_category"]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = ImageSerializer(instance.image).data
        return representation

    def create(self, validated_data):
        # check if user is a part of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a Category.")

        # creates category
        productCategory = ProductCategory.objects.create(**validated_data)

        # assign perms to group
        assign_perm('change_productcategory', group, productCategory)
        assign_perm('delete_productcategory', group, productCategory)
        return productCategory




class ProductListSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True, write_only=True)
    class Meta:
        model = ProductList
        fields = ["id", "name", "slug", "featured", "category", "image", "products"]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Replace the images field with serialized images data
        representation['image'] = ImageSerializer(instance.image.all(), many=True).data
        representation['products'] = ProductUserSerializer(instance.products.all(), many=True).data
        return representation

    def create(self, validated_data):

        # check if user is appart of sales
        group = Group.objects.get(name="sale")
        user = self.context['request'].user
        if not user.groups.filter(name='sale').exists():
            raise PermissionDenied("You don't have permission to create a ProductList.")

        # pops data that will be set later, and creates ProductList
        products = validated_data.pop('products', [])
        images_data = validated_data.pop('image', [])
        category_data = validated_data.pop('category', [])
        productlist = ProductList.objects.create(**validated_data)

        # change productlist to add products
        productlist.products.set(products)
        productlist.image.set(images_data)
        productlist.category.set(category_data)


        # assign perms to group
        assign_perm('change_productlist', group, productlist)
        assign_perm('delete_productlist', group, productlist)
        return productlist



class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'modified_at', 'deleted_at']

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
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ['id', "author", 'created_at', 'modified_at', 'deleted_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        author_data = UserSerializer(instance.author).data
        first_name = author_data.get('first_name')
        representation['author'] = first_name
        return representation

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
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    class Meta:
        model = OrderItems
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'modified_at', 'deleted_at']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Replace the images field with serialized images data
        representation['product'] = ProductUserSerializer(instance.product).data
        return representation

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


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

    def get_permissions(self):
        user = self.context['request'].user
        obj = self.instance

        # Check if the user has the required permission to view the object
        if not user.has_perm('view_orderdetails', obj):
            raise PermissionDenied("You do not have permission to view this Order.")

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
        if not user.has_perm('add_blogpost'):
            raise PermissionDenied("You don't have permission to create a blogpost.")

        # creates orderItems
        created_blog_post = BlogPost.objects.create(**validated_data)

        # Group perms
        assign_perm('change_blogpost', group, created_blog_post)

        return created_blog_post