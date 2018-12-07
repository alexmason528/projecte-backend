import os

from datetime import datetime
from simplecrypt import decrypt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


def authenticate(username, password):
    User = get_user_model()

    if not username or not password:
        return None

    if username:
        user_filter = User.objects.filter(Q(username=username) | Q(email=username))
    else:
        return None

    user = user_filter.first()

    if not user or not user.check_password(password):
        return None

    return user


def validate_token(token, token_type):
    User = get_user_model()

    if token_type == 'email_verify_token':
        filter = User.objects.filter(email_verify_token=token)
    elif token_type == 'password_reset_token':
        filter = User.objects.filter(password_reset_token=token)
    else:
        raise ValidationError('Token type is not valid.')

    if filter.count() != 1:
        raise ValidationError('Token is not valid.')

    user = filter.first()

    payload = get_payload_from_token(token)

    if not payload:
        raise ValidationError('Token is not valid.')

    id, issued_at = payload.split('-')

    elapsed = datetime.now() - datetime.fromtimestamp(float(issued_at))

    if user.id != int(id):
        raise ValidationError('Token is not valid.')

    if elapsed > settings.JWT_AUTH['JWT_EXPIRATION_DELTA']:
        raise ValidationError('Token is expired.')

    return user


def get_user_from_email(email):
    User = get_user_model()

    filter = User.objects.filter(email=email)

    if filter.count() != 1:
        raise ValidationError('User with provided email is not registered.')

    return filter.first()


def get_jwt_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token


def get_payload_from_token(token):
    try:
        token_encrypt_key = os.environ.get('TOKEN_ENCRYPT_KEY')
        token_as_bytes = bytes.fromhex(token)
        payload = decrypt(token_encrypt_key, token_as_bytes).decode('utf-8')
    except:
        return None

    return payload
