from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)