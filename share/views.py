from rest_framework import viewsets
from share.serializers import SharedLinkSerializer
from share.models import SharedLink
from audit.models import Audit
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status


class SharedLinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SharedLinkSerializer

    def get_queryset(self):
        return SharedLink.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def download(self, request: HttpRequest, pk):
        obj = SharedLink.objects.filter(link=pk).first()

        if not obj:
            return Response({"error": "Link não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if not obj.is_active:
            return Response({
                "error":"Link para download não ativo."
            }, status=status.HTTP_400_BAD_REQUEST)
        if obj and obj.expired < timezone.now():
            return Response({
                "error":"Link para download expirado."
            }, status=status.HTTP_400_BAD_REQUEST)

        ip_user = request.META.get('REMOTE_ADDR')
        browser_agent = request.headers.get('User-Agent','Desconhecido')
        user_user_link_download = request.user if request.user.is_authenticated else None

        Audit.objects.create(
            dono=user_user_link_download,
            action="DOWNLOAD",
            content_object=obj,
            ip_address=ip_user,
            cache_data={
                "user_agent": browser_agent,
                "arquivo_acessado_id": str(obj.file.uploaded_file.name) if obj.file else str(obj.folder.id)
            }
        )
