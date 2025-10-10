from django.urls import path
from .views import SignupView, LoginView, LogoutView, AllUsersView, MeView, UserProfileDetailView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', AllUsersView.as_view(), name='all_users'),
    path('user/me', MeView.as_view(), name='me'),
    path("users/<str:username>/", UserProfileDetailView.as_view(), name="user-profile"),

]
