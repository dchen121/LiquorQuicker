from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name='profile'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/auth_user/$', views.auth_user, name='auth_user'),
    url(r'^signup/$', views.sign_up, name = 'signup'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
]
