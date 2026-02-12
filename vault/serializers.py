import mimetypes

from rest_framework import serializers

from core.serializers import UserSerializer
from vault.models import File, Folder
from vault.services import compress_file


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "parent", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "owner"]


class FileSerializer(serializers.ModelSerializer):
    owner_details = UserSerializer(source="owner", read_only=True)
    compactar = serializers.BooleanField(write_only=True, required=False, default=False)
    compactar_tipo = serializers.CharField(
        write_only=True, required=False, default="MEDIO"
    )

    class Meta:
        model = File
        fields = [
            "id",
            "owner_details",
            "folder",
            "name",
            "file_size",
            "types",
            "created_at",
            "updated_at",
            "file",
            "compactar",
            "compactar_tipo",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Verifica se a flag compactar está ativa.
        Se sim, compacta o arquivo antes de salvar.
        Se não, mantém o arquivo original.
        """
        compactar_arquivo = validated_data.pop("compactar", False)
        compactar_tipo = validated_data.pop("compactar_tipo", None)
        arquivo_original = validated_data["file"]

        if compactar_arquivo:
            tipo_compactacao = compactar_tipo or "MEDIO"
            try:
                validated_data["file"] = compress_file(
                    file=arquivo_original, zip_type=tipo_compactacao
                )
            except ValueError as e:
                raise serializers.ValidationError(
                    {"compactar_tipo": str(e)}
                ) from None

        arquivo_final = validated_data["file"]
        validated_data["name"] = arquivo_final.name
        validated_data["file_size"] = getattr(arquivo_final, "size", None) or len(
            arquivo_final.read()
        )
        arquivo_final.seek(0)

        tipo_arquivo, _ = mimetypes.guess_type(arquivo_final.name)
        validated_data["types"] = tipo_arquivo or "tipo não localizado"

        return super().create(validated_data)
