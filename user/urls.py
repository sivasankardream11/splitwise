from django.urls import path
from user.views import (CreateUser, OTPVerify, GenerateOTP, ResetPassword,
                        UserTokenObtainPairView, UserTokenRefreshView,
                        UserTokenBlacklistView, UserForgotPassword, UserInfoView, DeleteUser)

urlpatterns = [
    path('register/', CreateUser.as_view(), name='create-user'),  # Endpoint for user registration
    path('verify-otp/', OTPVerify.as_view(), name='verify-otp'),  # Endpoint for OTP verification
    path('generate-otp/', GenerateOTP.as_view(), name='generate-otp'),  # Endpoint for OTP generation
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),  # Endpoint for resetting password
    path('login/', UserTokenObtainPairView.as_view(), name='user-login'),  # Endpoint for user login
    path('refresh-token/', UserTokenRefreshView.as_view(), name='refresh-token'),  # Endpoint for token refresh
    path('forgot-password/', UserForgotPassword.as_view(), name='user-forgot_password'),  # Endpoint for forgot password
    path('logout/', UserTokenBlacklistView.as_view(), name='user-logout'),  # Endpoint for user logout
    path('user-info/', UserInfoView.as_view(), name='user-info'),  # Endpoint for managing user information (create, retrieve, update)
    path('delete-account/', DeleteUser.as_view(), name='delete-account'),  # Endpoint for deleting user account


]