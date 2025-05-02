from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import RegisterSerializer
from account.serializer import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({"data": user.username}, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Test(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = JWTAuthentication,
    def get(self, request):
        return Response({"data": request.user.username}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class LogoutView(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = JWTAuthentication,
    def post(self, request):
        data = request.data
        refresh = RefreshToken(data.get('refresh'))
        refresh.blacklist()
        return Response({'msg':'done'})