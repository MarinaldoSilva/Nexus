from rest_framework import serializers
from vault.models import File
from core.serializers import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    
    owner_details = UserSerializer(source='owner', read_only=True)
        
    class Meta:
        model = File
        fields = ["id","owner_details", "name", "file_size", "types", "created_at","updated_at", "file"]
        read_only_fields = ["id","owner","file_size","created_at", "updated_at"]
        