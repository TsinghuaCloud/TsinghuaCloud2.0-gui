from django.conf.urls.defaults import patterns, url
from .utils import patch_middleware_get_user

patch_middleware_get_user()


urlpatterns = patterns('openstack_auth.views',
    url(r"^login/$", "login", name='login'),
    url(r"^logout/$", 'logout', name='logout'),
    url(r"^register/$", "register", name='register'),
    
#add index3
#    url(r"^index3/$", 'index3', name='index3'),
    url(r'^switch/(?P<tenant_id>[^/]+)/$', 'switch', name='switch_tenants'),
    url(r'^switch_services_region/(?P<region_name>[^/]+)/$', 'switch_region',
        name='switch_services_region')
)
