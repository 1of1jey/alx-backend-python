from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth

urlpatterns = [
    path('login/', auth.login, name='login'),
    path('register/', auth.register, name='register'),
    path('logout/', auth.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', auth.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', auth.user_profile, name='user_profile'),
    path('profile/update/', auth.update_profile, name='update_profile'),
]