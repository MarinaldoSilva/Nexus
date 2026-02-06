from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from vault.models import File
from vault.serializers import FileSerializer
from vault.permissions import IsAdmin
from vault.services import compress_file_lzma


class FileViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        if self.action == 'compress_standalone':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='comprimir')
    def compress_standalone(self, request):
        """
        Endpoint utilitário para compressão avulsa (sem salvar no banco).
        Acessível em: /api/files/comprimir/
        """
        obj_file = request.FILES.get('file')
        if not obj_file:
            return Response({
                "error": "Arquivo não enviado"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        compressed = compress_file_lzma(obj_file)
        
        response = HttpResponse(compressed, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{compressed.name}"'
        response['Content-Length'] = compressed.size
        return response