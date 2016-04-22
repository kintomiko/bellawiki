from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(views.router.urls)),
    url(r'^work_details/search$', views.search_work),
    url(r'^work_details/save$', views.save_work),
    url(r'^work_details/add_file$', views.add_file),
    url(r'^work_details/add_work_tag$', views.add_work_tag),
    url(r'^work_details/del_work_tag$', views.del_work_tag),
    url(r'^file_details/save_file$', views.save_file),
    url(r'^file_details/add_file_tag$', views.add_file_tag),
    url(r'^file_details/del_file_tag$', views.del_file_tag),
    url(r'^file_timeline_json$', views.file_timeline_json),
    url(r'^time_line$', views.time_line),
    url(r'^proxy$', views.proxy),
    url(r'^upload_list$', views.upload_list),
    url(r'^upload$', views.upload),
    url(r'^work_details/$', views.create_or_edit_work),
    url(r'^work_up/$', views.up),
    url(r'^file_details$', views.edit_file),
    url(r'^tag_index$', views.tag_index),
    url(r'^$', views.index, name='index'),
    url(r'work_today', views.today),
)
