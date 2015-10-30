from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name='profile'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/auth_user/$', views.auth_user, name='auth_user'),
    url(r'^account/signup/$', views.sign_up, name = "signup"),
]
