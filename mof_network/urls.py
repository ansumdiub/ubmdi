from django.conf.urls import url
from django.conf import settings
from . import views
from django.views.generic import RedirectView
from django.conf.urls.static import static

# SET THE NAMESPACE!
app_name = 'mof'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^d3map/$', views.MapView.as_view(), name='map_view'),
    # url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^drafts/$', views.DraftListView.as_view(), name='mof_draft_list'),
    url(r'^mof/(?P<pk>[\d\w]+)/comment/$', views.add_comment_to_mof, name='add_comment_to_mof'),
    url(r'^comment/(?P<pk>[\d\w]+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>[\d\w]+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^mof/$', views.MofListView.as_view(), name='mof_list'),
    url(r'^mof/(?P<pk>[A-Z\d]+)/$', views.MofDetailView.as_view(), name='mof_detail'),
    url(r'^mof/new/$', views.MofCreateView.as_view(), name='mof_new'),
    url(r'^mof/update/(?P<pk>[A-Z\d]+)/$', views.MofUpdateView.as_view(), name='mof_update'),
    url(r'^mof/delete/(?P<pk>[A-Z\d]+)/$', views.MofDeleteView.as_view(), name='mof_delete'),
    url(r'^mof/approve/(?P<pk>[A-Z\d]+)/$', views.MofDetailView.as_view(), name='mof_approve'),
    url(r'^d3map/ajax/add/', views.ajax_render, name='ajax_add'),
]
