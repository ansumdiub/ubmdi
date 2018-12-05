from django.conf.urls import url
from . import views

# SET THE NAMESPACE!
app_name = 'mof_network'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mapView/$', views.map_view, name='map_view'),
]
