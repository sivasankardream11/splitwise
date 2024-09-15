# Import necessary modules
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.models import User, OTPModel, UserInfo
from user.serializers import UserModelSerializer, OTPSerializer, EmailSerializer, UserTokenObtainPairSerializer, UserInfoSerializer
from utils.generate_otp import generate_otp
from utils.email import send_email
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenBlacklistSerializer



# Function to check if user exists in the database with a given email
def check_user_with_mail(email, model):
    try:
        model_obj = model.objects.get(email=email)
    except Exception as e:
        model_obj = False

    return model_obj

# API view for creating a user
class CreateUser(APIView):
    """
    API endpoint for creating a user.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            user = check_user_with_mail(request.data.get('email'), User)
            if user and request.data.get('password'):
                if not user.is_active:
                    otp = generate_otp()
                    otp_object = check_user_with_mail(request.data.get('email'), OTPModel)
                    email_status = send_email(
                        subject='Email Verification',
                        message='otp is {}'.format(otp),
                        to_mail=request.data.get('email')
                    )
                    if not email_status:
                        context = {
                            'message': 'Email could not be sent!, Please try later.'
                        }
                        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                    elif email_status and otp_object:
                        context = {
                            'message': 'OTP is send to the email , Please Varify'
                        }
                        otp_object.otp = otp
                        otp_object.save()
                        return Response(data=context, status=status.HTTP_200_OK)
                    elif email_status and not otp_object:
                        otp_serializer = OTPSerializer(data={'email': request.data.get('email'), 'otp': otp})
                        if otp_serializer.is_valid():
                            otp_serializer.save()
                            context = {
                                'message': 'OTP is send to the email , Please Varify'
                            }
                            return Response(data=context, status=status.HTTP_200_OK)
                        else:
                            context = {
                                'message': 'Something went wrong.'
                            }
                            return Response(data=context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif user.is_active:
                    context = {
                        'message': 'Email already existed.'
                    }
                    return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

            user_serializer = UserModelSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                otp = generate_otp()
                email_status = send_email(
                    subject='Email Verification',
                    message='otp is {}'.format(otp),
                    to_mail=request.data.get('email')
                )
                if not email_status:
                    context = {
                        'message': 'Email could not be sent!, Please try later.'
                    }
                    return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                elif email_status:
                    otp_serializer = OTPSerializer(data={'email': request.data.get('email'), 'otp': otp})
                    if otp_serializer.is_valid():
                        otp_serializer.save()
                        context = {
                            'message': 'User created Successfully, OTP is send to the email , Please Varify'
                        }
                        return Response(data=context, status=status.HTTP_201_CREATED)
            else:
                return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OTPVerify(APIView):
    """
    API endpoint for verifying OTP and activating user account.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = check_user_with_mail(request.data.get('email'), User)

        if user:
            if not user.is_active:
                otp_obj = check_user_with_mail(request.data.get('email'), OTPModel)
                if not otp_obj:
                    context = {
                        'message': 'Register first before verify to user.',
                    }
                    return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                else:
                    current_time = int(timezone.now().timestamp())
                    adjusted_updated_at = otp_obj.updated_at + timedelta(minutes=10)
                    adjusted_updated_at = int(adjusted_updated_at.timestamp())
                    if otp_obj.otp != request.data.get('otp'):
                        context = {
                            'message': 'OTP not valid.',
                        }
                        return Response(data=context, status=status.HTTP_406_NOT_ACCEPTABLE)
                    elif current_time > adjusted_updated_at:
                        context = {
                            'message': 'OTP expired.',
                        }
                        return Response(data=context, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        user.is_active = True
                        user.save()
                        otp_obj.delete()
                        context = {
                            'message': 'Verified successfully.',
                        }
                        return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    'message': 'User already verified, please login.',
                }
                return Response(data=context, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            context = {
                'message': 'Register first before verify to user.',
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class GenerateOTP(APIView):
    """
    API endpoint for generating and sending OTP to the user's email for account verification.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email_serializer = EmailSerializer(data=request.data)
        if email_serializer.is_valid():
            user = check_user_with_mail(email_serializer.validated_data.get('email'), User)
            if user:
                if not user.is_active:
                    otp = generate_otp()
                    otp_obj = check_user_with_mail(request.data.get('email'), OTPModel)
                    if not otp_obj:
                        email_status = send_email(
                            subject='Email Verification',
                            message='otp is {}'.format(otp),
                            to_mail=request.data.get('email')
                        )
                        if not email_status:
                            context = {
                                'message': 'Email could not be sent!, Please try later.'
                            }
                            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            context = {
                                'message': 'OTP is send to the email , Please Varify'
                            }
                            otp_serializer = OTPSerializer(data={'email': request.data.get('email'), 'otp': otp})
                            if otp_serializer.is_valid():
                                otp_serializer.save()
                            return Response(data=context, status=status.HTTP_200_OK)
                    else:
                        email_status = send_email(
                            subject='Email Verification',
                            message='otp is {}'.format(otp),
                            to_mail=request.data.get('email')
                        )
                        if not email_status:
                            context = {
                                'message': 'Email could not be sent!, Please try later.'
                            }
                            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            context = {
                                'message': 'OTP is send to the email , Please Varify'
                            }
                            otp_obj.otp = otp
                            otp_obj.save()
                            return Response(data=context, status=status.HTTP_200_OK)

                else:
                    context = {
                        'message': 'user already verified, please do login.'
                    }
                    return Response(data=context, status=status.HTTP_409_CONFLICT)

            else:
                context = {
                    'message': 'user not exist please register first.'
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                'message': 'Enter valid email.'
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
    API endpoint for resetting user passwords.
    ---
    request_serializer: ResetPasswordSerializer
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Reset the user password.
        """
        try:
            user = request.user
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if old_password == new_password :
                context = {
                    'message': 'New password should be different from the old password'
                }
                return Response (data=context, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(old_password):
                context = {
                    'message': 'Old password is incorrect'
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            context = {
                'message': 'Password has been changed successfully'
            }
            return Response(data=context, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(str(e))
            context = {
                'message': 'Internal server error'
            }
            return Response(data=context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserForgotPassword(APIView):
    """
    API endpoint for handling forgot password functionality.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        API endpoint for sending OTP to reset password via email.
        """
        email = request.query_params.get('email')
        user = check_user_with_mail(email, User)
        if user:
            otp = generate_otp()
            email_status = send_email(
                subject='Forgot Password OTP',
                message='otp is {}'.format(otp),
                to_mail=email
            )
            if not email_status:
                context = {
                    'message': 'Email could not be sent!, Please try later.'
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
            elif email_status:
                context = {
                    'message': 'OTP is send to the email , Please Varify'
                }
                otp_serializer = OTPSerializer(data={'email': email, 'otp': otp})
                if otp_serializer.is_valid():
                    otp_serializer.save()
                return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'User not exists.'
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        API endpoint for resetting password using OTP.
        """
        email = request.data.get('email')
        otp = request.data.get('otp')
        password = request.data.get('new-password')
        otp_object = check_user_with_mail(email, OTPModel)
        if otp_object and otp_object.otp == otp:
            user = check_user_with_mail(email, User)
            if user:
                user.set_password(password)
                user.save()

                otp_object.delete()

                context = {
                    "message": "Password updated successfully."
                }
                return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    "message": "User not found."
                }
                return Response(data=context, status=status.HTTP_404_NOT_FOUND)
        else:
            context = {
                "message": "Invalid OTP."
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    """
    API endpoint for creating, retrieving, and updating user information.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST method to create user information.
        """
        data = request.data.copy()  # Create a copy of request data
        data['user'] = request.user.id  # Assign authenticated user ID to 'user' field
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'message': 'User info created successfully',
                'user_info': serializer.data
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                'message': 'Failed to create user info',
                'errors': serializer.errors
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        GET method to retrieve user information.
        """
        user_info = UserInfo.objects.filter(user=request.user).first()
        if user_info:
            serializer = UserInfoSerializer(user_info)
            context = {
                'message': 'User info retrieved successfully',
                'user_info': serializer.data
            }
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'User info not found',
            }
            return Response(data=context, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        """
        PUT method to update user information.
        """
        user_info = UserInfo.objects.filter(user=request.user).first()
        if user_info:
            # Check if any fields are provided in the request data
            if not request.data:
                context = {'message': 'No data provided for update'}
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserInfoSerializer(user_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {'message': 'User info updated successfully'}
                return Response(data=context, status=status.HTTP_200_OK)
            else:
                context = {
                    'message': 'Failed to update user info',
                    'errors': serializer.errors
                }
                return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {'message': 'User info not found'}
            return Response(data=context, status=status.HTTP_404_NOT_FOUND)


class UserTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint for obtaining JWT token pair for user authentication.
    """
    permission_classes = [AllowAny]
    serializer_class = UserTokenObtainPairSerializer


class UserTokenRefreshView(TokenRefreshView):
    """
    API endpoint for refreshing JWT token for user authentication.
    """
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer


class UserTokenBlacklistView(TokenBlacklistView):
    """
    API endpoint for blacklisting JWT token for user authentication.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TokenBlacklistSerializer


class DeleteUser(APIView):
    """
    API endpoint for deleting a user account (soft delete).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """
        DELETE method to deactivate a user account.
        """
        user = request.user
        user.is_active = False  # Deactivate the user account
        user.save()
        context = {
            'message': 'User account deactivated (soft delete).'
        }
        return Response(data=context, status=status.HTTP_204_NO_CONTENT)

