from rest_framework import serializers
from share.models import SharedLink
from django.utils import timezone
from datetime import timedelta

class SharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedLink
        fields = "__all__"

        read_only_fields = ["link","created_at","created_by"]
        extra_kwargs = {
            'expired': {
                'required': False,
                'allow_null': True
            }
        }

    def validate(self, attrs:dict)->dict:
        expired = attrs.get('expired', None)
        file = attrs.get('file', None)
        folder = attrs.get('folder', None)

        if not expired:
            attrs['expired'] = timezone.now() + timedelta(hours=6)

        elif expired <= timezone.now():
            raise serializers.ValidationError("A data de expiração deve ser posterior a atual.")

        if bool(file) == bool(folder):
            raise serializers.ValidationError("É necessário ao menos m ficheiro para ser gerado o link.")
        return attrs



