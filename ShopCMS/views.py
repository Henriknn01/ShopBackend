import json

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




# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
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

    def subcategories(self, catagoryNumber):
        category = ProductCategory.objects.get(id=catagoryNumber)
        subcategories = category.get_all_subcategories()
        return subcategories

    def get_catagory_name(self, catagoryNumber):
        return ProductCategory.objects.get(id=catagoryNumber).name



    @action(detail=True, methods=['get'])
    def get_sections(self, request, pk=None):

        sendback = {
            "catSection": {
                "featuredCollection": [],
                "sections": [
                    {
                        "catagoryNumber": 4,
                        "id": "allcats",
                        "Name": "For all cats",
                        "items": []
                    },
                    {
                        "catagoryNumber": 5,
                        "id": "OutdoorCat",
                        "Name": "OutdoorCat",
                        "items": []
                    },
                    {
                        "catagoryNumber": 6,
                        "id": "brands",
                        "Name": "Brands",
                        "items": []
                    }
                ]
            },
            "dogSection": {
                "featuredCollection": [],
                "sections": [
                    {
                        "catagoryNumber": 7,
                        "id": "alldogs",
                        "Name": "For all dogs",
                        "items": []
                    },
                    {
                        "catagoryNumber": 8,
                        "id": "Doghealth",
                        "Name": "DogHealth",
                        "items": []
                    },
                    {
                        "catagoryNumber": 9,
                        "id": "brands",
                        "Name": "Brands",
                        "items": []
                    }
                ]
            },
            "miscSection": {
                "featuredCollection": [],
                "sections": [
                    {
                        "catagoryNumber": 29,
                        "id": "birds",
                        "Name": "Birds",
                        "items": []
                    },
                    {
                        "catagoryNumber": 30,
                        "id": "Reptiles",
                        "Name": "Reptiles",
                        "items": []
                    },
                    {
                        "catagoryNumber": 31,
                        "id": "brands",
                        "Name": "Brands",
                        "items": []
                    }
                ]
            }
        }

        for section_name in ["catSection", "dogSection", "miscSection"]:

            sendback[section_name]["featuredCollection"] = []

        for section_name in ["catSection", "dogSection", "miscSection"]:
            i = 0
            for sections in sendback[section_name]["sections"]:
                subcats = self.subcategories(sections["catagoryNumber"])
                itemsArray = []
                for CatNumber in subcats:
                    itemsArray.append({ "name": self.get_catagory_name(CatNumber), "href": f"/categories/{CatNumber}"})
                sendback[section_name]["sections"][i]["items"] = itemsArray
                i = i + 1
        return JsonResponse(sendback)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductUserSerializer


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

    def perform_create(self, serializer):
        serializer.save()



class ProductListViewSet(viewsets.ModelViewSet):
    queryset = ProductList.objects.all()
    serializer_class = ProductListSerializer

    def perform_create(self, serializer):
        serializer.save()

    def featured_list(self, tag_id):
        featuredlist = ProductList.featured_lists(ProductList.objects, tag_id)
        return featuredlist

    @action(detail=True, methods=['get'])
    def get_featured_list(self, request, pk=None):

        sendback = {
            "catSection": {
                "tag_id":1 ,
                "featuredCollection": []
            },
            "dogSection": {
                "tag_id":2,
                "featuredCollection": []
            },
            "miscSection": {
                "tag_id":3,
                "featuredCollection": []
            }
        }

        for section_name in ["catSection", "dogSection", "miscSection"]:
            setArray = []
            featuredCollections = self.featured_list(sendback[section_name]["tag_id"])
            for prod_list in featuredCollections:
                setArray.append({"name": prod_list.name, "href": prod_list.id, "imageSrc": prod_list.image.first().src, "imageAlt": prod_list.image.first().alt})
            sendback[section_name]["featuredCollection"] = setArray
        print(sendback)
        return JsonResponse(sendback)



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

    def get_queryset(self):
        queryset = OrderDetails.objects.all()
        user = self.request.user
        return get_objects_for_user(user, "view_paymentdetails", queryset)


    def perform_create(self, serializer):
        serializer.save()

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save()

