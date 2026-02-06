from rest_framework import serializers
from vault.models import File
from core.serializers import UserSerializer
from vault.services import compress_file_lzma


class FileSerializer(serializers.ModelSerializer):
    
    owner_details = UserSerializer(source='owner', read_only=True)
    compactar = serializers.BooleanField(write_only=True, required=False, default=False)
    
    class Meta:
        model = File
        fields = [
            "id",
            "owner_details",
            "name",
            "file_size",
            "types",
            "created_at",
            "updated_at",
            "file",
            "compactar",
        ]
        read_only_fields = [
            "id",
            "owner",
            "file_size",
            "created_at",
            "updated_at",
            "types",
        ]
    
    def create(self, validated_data):
        """
        Verifica se a flag compactar esta ativa, e caso esteja o campo 'file' do validated_data vai receber o arquivo compactado, caso False, removemos o campo do validated_data.
        """
        compactar_arquivo = validated_data.pop('compactar', False)
        if compactar_arquivo:
            data = validated_data['file']
            validated_data['file'] = compress_file_lzma(file=data)
        return super().create(validated_data) 