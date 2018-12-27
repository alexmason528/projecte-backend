import os
import time

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from simplecrypt import encrypt


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    email_verify_token = models.CharField(max_length=256, blank=True, null=True)
    password_reset_token = models.CharField(max_length=256, blank=True, null=True)
    photo = models.ImageField(upload_to="users/photos", blank=True, null=True)

    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def email_verified(self):
        return not self.email_verify_token

    @property
    def estimation_count(self):
        return len(self.estimations.all())

    @property
    def total_amount(self):
        return sum(estimation.value for estimation in self.estimations.all())

    @property
    def accuracy(self):
        return 7.5

    def generate_token(self, token_type):
        if not token_type in ['password_reset_token', 'email_verify_token']:
            raise ValidationError('Token type is not valid.')

        issued_at = time.time()
        payload = '{}-{}'.format(self.id, issued_at)
        token = encrypt(os.environ.get('TOKEN_ENCRYPT_KEY'), payload).hex()

        setattr(self, token_type, token)
        self.save()

        return token

    def send_email(self, email_type):
        if not email_type in ['password', 'verify']:
            raise ValidationError('Email type is not valid.')

        if email_type == 'password':
            url = 'PASSWORD_RESET_URL'
            token_type = 'password_reset_token'
            template = 'password_reset_email.html'
        elif email_type == 'verify':
            url = 'EMAIL_VERIFY_URL'
            token_type = 'email_verify_token'
            template = 'verification_email.html'

        try:
            link = '{}?code={}'.format(os.environ.get(url), self.generate_token(token_type))
            company = os.environ.get('COMPANY')

            template_param = {
                'name': self.username,
                'company': company,
                'link': link,
            }

            subject = 'Welcome to {}'.format(company)
            from_email = os.environ.get('NO_REPLY_EMAIL_ADDRESS')
            message = render_to_string(template, template_param)

            self.email_user(
                subject=subject,
                message='',
                html_message=message,
                from_email=from_email,
            )
        except:
            raise ValidationError('Failed to send {} email.'.format(
                'password reset' if email_type == 'password' else 'verification'))
