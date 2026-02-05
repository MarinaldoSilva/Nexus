from django.shortcuts import get_object_or_404
from core.models import User
from core.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)
    
    def get(self, request):
        user_details = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(user_details, many=True, context={'request':request})
        return Response({
            'result':serializer.data
        },status=status.HTTP_200_OK)

class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user = request.user
        
        serializer = UserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'result':serializer.data
        },status=status.HTTP_200_OK)
 

class AccountInactiveView(APIView):
    """
    fallback para quando um user tentar logar/registrar mas a conta está inativa
    """
    def get(self, request):
        return Response({
            'detail':'Sua conta foi criada com sucesso, porém seu usúario esta inativo, verifique seu E-mail'
        })
