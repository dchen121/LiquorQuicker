from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.MapView.as_view(), name='map'),
    url(r'^google-site-verification: google425a70456562b518.html$', TemplateView.as_view(template_name='google-verification.html')),
    url(r'^store/(?P<pk>[0-9]+)/$', views.store_profile, name="store"),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^store/(?P<pk>[0-9]+)/add_review/$', views.add_review, name='add_review'),
]
