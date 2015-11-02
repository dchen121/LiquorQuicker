from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MapView.as_view(), name='map'),
]
