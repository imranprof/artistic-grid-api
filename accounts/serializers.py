from rest_framework import serializers
from .models import User
from imr_grid_api.models import Post, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators = [validate_password])

    class Meta: 
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        #allow login with either username or email

        user = authenticate(
            request=self.context.get("request"),
            username=username_or_email,
            password=password
        )

        if user is None:
            # Try authenticate with email
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(
                    request=self.context.get("request"),
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                pass
        
        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password"
            )
        
        data = super().validate({
            'username': user.username,
            'password': password
        })

        #Add custom user data to the response

        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

        return data

# this user list for development purposes only
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


#for user profile show
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["about", "avatar_url", "name"]

class UserProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile", "posts"]

    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj, status="published").order_by("-created_at")
        return [{"id": p.id, "title": p.title, "image_url": p.image_url} for p in posts]