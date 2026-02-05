from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vault.models import File
from vault.serializers import FileSerializer
from rest_framework.permissions import IsAuthenticated
from vault.permissions import IsAdmin


class FileListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        files = File.objects.filter(owner=request.user)
        
        serializer = FileSerializer(files, many=True, context={'request':request})
        return Response({
            "result": serializer.data
        },status=status.HTTP_200_OK)
    
class FileCreateAPIView(APIView):
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
        
    
    
        
        
        