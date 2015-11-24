from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', views.ProfileView.as_view(), name='profile'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^login/auth_user/$', views.auth_user, name='auth_user'),
    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^search/$', views.user_search, name='search'),
    url(r'^notfound/$',views.UserNotFound.as_view(), name='notfound')
]
