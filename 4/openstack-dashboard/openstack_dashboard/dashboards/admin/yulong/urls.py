
from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from openstack_dashboard.dashboards.admin.yulong import views

urlpatterns = patterns('openstack_dashboard.dashboards.admin.yulong.views',
    url(r'^$', views.IndexView.as_view(), name='index')
)  
