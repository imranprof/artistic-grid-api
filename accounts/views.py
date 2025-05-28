from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken.for_user(serializer.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "message": "Login successful",
            "user": serializer.validated_data["user"]
        }, status=status.HTTP_200_OK)


        #set http-only cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age= 15 * 60,  # 15 minutes
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age= 7 * 24 * 60 * 60,  # 7 days
        )
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

