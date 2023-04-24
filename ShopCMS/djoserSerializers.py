from djoser import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()

class UserCreateSerializer(serializers.UserCreateSerializer):
    class Meta(serializers.UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']


class ShopCMSTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['role'] = user.groups.first().name

        return token
