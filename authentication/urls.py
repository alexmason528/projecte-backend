from django.conf.urls import url

from .views import LogInView, RegisterView, VerifyEmailView, PasswordResetView, ProfileView

urlpatterns = [
    url(r'^login/$', LogInView.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^verify-email/$', VerifyEmailView.as_view()),
    url(r'^password-reset/$', PasswordResetView.as_view()),
    url(r'^profile/$', ProfileView.as_view()),
]
