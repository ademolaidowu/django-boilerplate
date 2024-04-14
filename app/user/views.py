from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from app.core.renderers import DefaultRenderer
from .models import User
from .serializers import (
    RegisterEmailSerializer,
    RegisterSendSerializer,
    RegisterVerifySerializer,
    RegisterInfoSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserOTPSerializer,
)


class GenerateOTPView(generics.GenericAPIView):
    """
    API view for generating and sending OTP codes when requested to users
    """

    serializer_class = UserOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterEmailView(generics.GenericAPIView):
    """
    API View to Register a user by collecting email, password and sending OTP code for verification
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User registered successfully. Kindly verify email to proceed", "result": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class RegisterVerifyView(generics.GenericAPIView):
    """
    A class containing API View to confirm user email by OTP verification
    """

    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RegisterSendSerializer
        return RegisterVerifySerializer

    def get(self, request, *args, **kwargs):
        print(request.query_params)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "OTP code has been sent to email", "result": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Email has been confirmed"}, status=status.HTTP_200_OK)


class RegisterInfoView(generics.GenericAPIView):
    """
    A class containing API View to update information after user is created
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterInfoSerializer

    def put(self, request, *args, **kwargs):
        instance = request.user.profile

        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User Profile registration has been completed", "result": serializer.data},
            status=status.HTTP_200_OK,
        )


class LoginView(generics.GenericAPIView):
    """
    API view to login user and provide auth tokens
    """

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "User logged in successfully", "result": serializer.data},
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    """
    API view to logout user from a single device
    """

    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
