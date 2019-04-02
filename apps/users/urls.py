# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import LoginView,LogoutView,RegisterView,ProfileHomeView,ProfileHelpView,UpdateProfileView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^profile/$', ProfileHomeView.as_view(), name="profile"),
    url(r'^update_profile/$', UpdateProfileView.as_view(), name="update_profile"),
    url(r'^help/$', ProfileHelpView.as_view(), name="help"),
]