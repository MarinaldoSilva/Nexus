from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from vault.models import File, Folder
from vault.serializers import FileSerializer, FolderSerializer
from vault.permissions import IsAdmin
from vault.services import compress_file


class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FolderSerializer
    
    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
        obj_file = request.FILES.get('file')
        if not obj_file:
            return Response({
                "error": "Arquivo não enviado"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tipo = request.data.get('compactar_tipo', 'MEDIO')
        
        try:
            compressed = compress_file(obj_file, zip_type=tipo)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        response = HttpResponse(compressed, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{compressed.name}"'
        response['Content-Length'] = compressed.size
        return response