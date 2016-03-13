from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^verify_dzwm', views.verify_dzwm),
    url(r'^cache/(?P<domain>.*)/(?P<machine_id>.*)', views.set_cache),
    url(r'^cache/(?P<domain>.*)', views.view_create_cache),
    url(r'^get_dzwm', views.get_dzwm),
    url(r'^get_proxy', views.get_proxy),
    url(r'^add_proxy', views.add_proxy),
    url(r'^del_proxy', views.del_proxy),
    url(r'^set_all_dzwm', views.set_all_dzwm),
)
