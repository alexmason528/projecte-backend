from django.utils.translation import ugettext as _

from rest_framework import serializers, status
from rest_framework.response import Response

from rest_framework_jwt.serializers import JSONWebTokenSerializer

from .models import User

from .utils import authenticate, get_jwt_token


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password'),
        }

        if not credentials[self.username_field]:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)

        else:
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                return {
                    'token': get_jwt_token(user),
                    'user': user,
                }
            else:
                msg = _('Invalid username or password.')
                raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'photo', 'email_verified', 'estimation_count', 'total_amount', 'accuracy')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'photo', 'email_verified',
                  'estimation_count', 'total_amount', 'accuracy')
        read_only_fields = ('id', 'email_verified')
        extra_kwargs = {
            'password': {'write_only': True},
            'photo': {'required': False},
        }

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.generate_token('email_verify_token')
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'photo', 'email_verified',
                  'estimation_count', 'total_amount', 'accuracy', 'password')
        read_only_fields = ('id', 'email_verified')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'photo': {'required': False},
        }

    def update(self, instance, validated_data):
        email_changed = 'email' in validated_data and validated_data[
            'email'] != instance.email

        user = super(UserUpdateSerializer, self).update(
            self.instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])

        user.save()

        if email_changed:
            try:
                user.send_email('verify')
            except Exception as e:
                pass

        return user


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
