from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio',
                  'email', 'role',)

        model = User
        lookup_field = "username"
        lookup_value_regex = "[^/]+"


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(required=True)
