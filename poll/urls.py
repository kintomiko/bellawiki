from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^refresh/$', views.refresh),
    url(r'^get_json/$', views.get_date_json),
)

