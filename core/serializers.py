from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "type_user", "first_name", "last_name", "email", "is_active"]
        read_only_fields = ["id", "type_user"]
