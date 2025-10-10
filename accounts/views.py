from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.permissions import IsAuthenticated
from imr_grid_api.models import Profile
from rest_framework import generics


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # for create a profile also
            Profile.objects.create(user=user)
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
            secure=True, #for development
            samesite='None',  #LAX for production
            max_age= 15 * 60,  # 15 minutes
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,  #for development
            samesite='None',  #LAX for production
            max_age= 7 * 24 * 60 * 60,  # 7 days
        )
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token',samesite='None') #LAX for production
        response.delete_cookie('refresh_token',samesite='None') #LAX for production
        return response
    

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'detail': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({'message': 'Token refreshed'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',  #LAX for production
            max_age=15 * 60,
        )
        return response


# this user list for development purposes only
class AllUsersView(APIView):
    

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
#authorize user
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


#user profile views
class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = "username"

    def get_object(self):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)