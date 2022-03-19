from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from cards.models import *

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','username', 'email', 'password')


        
