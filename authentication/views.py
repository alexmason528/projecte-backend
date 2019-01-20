import os
import secrets

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from rest_framework_jwt.utils import (
    jwt_response_payload_handler,
    jwt_payload_handler,
    jwt_encode_handler,
)
from rest_framework_jwt.views import JSONWebTokenAPIView

from .models import User

from .serializers import (
    CustomJSONWebTokenSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    TokenVerifySerializer,
    PasswordResetSerializer,
)

from .utils import validate_token, get_jwt_token, get_user_from_email


class LogInView(JSONWebTokenAPIView):
    authentication_class = ()
    permission_class = ()
    serializer_class = CustomJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = {
            'token': token,
            'user': UserSerializer(user).data
        }

        return Response(response_data)


class RegisterView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        payload = jwt_payload_handler(user)
        response_data = {
            'token': jwt_encode_handler(payload),
            'user': serializer.data,
        }

        try:
            user.send_email('verify')
        except:
            pass

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class VerifyEmailView(CreateAPIView, RetrieveAPIView):
    serializer_class = TokenVerifySerializer

    def get_authenticators(self):
        if self.request.method == 'GET':
            return super(VerifyEmailView, self).get_authenticators()
        return []

    def get_permissions(self):
        if self.request.method == 'GET':
            return super(VerifyEmailView, self).get_permissions()
        return []

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            user.send_email('verify')
        except Exception as e:
            raise ValidationError('Failed to send verification email.')

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token')
        user = validate_token(token, 'email_verify_token')
        user.email_verify_token = None
        user.save()

        response_data = {
            'token': get_jwt_token(user),
            'user': UserSerializer(user).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetView(RetrieveUpdateAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PasswordResetSerializer
        return TokenVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = get_user_from_email(email)
        user.send_email('password')

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data.get('token')
        user = validate_token(token, 'password_reset_token')
        user.password_reset_token = None
        new_password = secrets.token_hex(15)
        user.set_password(new_password)
        user.save()

        response_data = {'new_password': new_password}

        return Response(response_data, status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView):
    parser_classes = (MultiPartParser, )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def retrieve(self, request):
        serializer_class = self.get_serializer_class()
        data = serializer_class(request.user).data
        return Response(data)

    def partial_update(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance=request.user,
            data=request.data,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'token': get_jwt_token(user),
            'user': UserSerializer(user).data,
        }

        return Response(response_data)


class UserInfoView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = ()
