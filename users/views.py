from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .serializers import RegisterSerializer, UserUpdateSerializer
from .permissions import IsOwner

class RegisterView(CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.save()
    data = serializer.data
    token = Token.objects.get(user=user)
    data['token'] = token.key
    headers = self.get_success_headers(data)
    return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class UserUpdateView(RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserUpdateSerializer
  permission_classes = [IsAuthenticated, IsOwner]