from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vault.models import File
from vault.serializers import FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from vault.permissions import IsAdmin
from vault.utils import compress_file_lzma


class FileListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        files = File.objects.filter(owner=request.user)
        
        serializer = FileSerializer(files, many=True, context={'request':request})
        return Response({
            "result": serializer.data
        },status=status.HTTP_200_OK)
    
class FileCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response({
            'results':serializer.data
        },status=status.HTTP_201_CREATED)

class FileUpdateAPIView(APIView):
    permission_classes = [IsAdmin]
    
    def get_object(self, pk):
        return get_object_or_404(File, pk=pk)
    
    def patch(self, request, pk):
        qs = self.get_object(pk=pk)
        
        serializer = FileSerializer(
            instance=qs,
            data=request.data,
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'result':serializer.data
        },status=status.HTTP_200_OK)
        
class FileDestroyAPIView(APIView):
    
    permission_classes = [IsAdmin]
    
    def get_object(self, pk):
            return get_object_or_404(File, pk=pk)
    
    def delete(self, request, pk):
        qs = self.get_object(pk=pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
class CompressFileAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]
    """
        Serviço de compatação de arquivos:
        Recebe um arquivo como parâmetro na função compress_file_lzma()
        faz a conversão dos dados e com o HttpResponse() transforma os dados binarios em
        um objeto que o django compreende e informa seu tipo, realiza o download do arquivo dirtamente no navegador. 
    """
    def post(self, request):
        obj_file = request.FILES.get('file')
        if not obj_file:
            return Response({
                "error": "Arquivo não enviado"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        compressed = compress_file_lzma(obj_file)
        response = HttpResponse(compressed,content_type='application/zip',)
        response['Content-Disposition'] =f'attachment; filename="{compressed.name}"'
        response['Content-Length'] = compressed.size
        return response        
    
    


        
        
    
        