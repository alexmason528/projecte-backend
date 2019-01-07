from django.conf.urls import url

from api.views import MyListingsView, WatchItemView, WatchItemDestroyView

from .views import LogInView, RegisterView, VerifyEmailView, PasswordResetView, ProfileView, UserInfoView

urlpatterns = [
    url(r'^login/$', LogInView.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^verify-email/$', VerifyEmailView.as_view()),
    url(r'^password-reset/$', PasswordResetView.as_view()),
    url(r'^profile/$', ProfileView.as_view()),
    url(r'^my-listings/$', MyListingsView.as_view()),
    url(r'^watchlist/(?P<item>(\w+))/$', WatchItemDestroyView.as_view()),
    url(r'^watchlist/$', WatchItemView.as_view()),
    url(r'^user-info/(?P<pk>(\w+))/$', UserInfoView.as_view()),
]
