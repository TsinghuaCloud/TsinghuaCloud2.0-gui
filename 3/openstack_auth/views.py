import logging

from threading import Thread

import base64,urllib,httplib,json,os
from urlparse import urlparse

from django import shortcuts
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import (login as django_login,
                                       logout_then_login as django_logout)
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.functional import curry
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt


from django.template import Template, Context
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response 
from django.http import HttpResponse
from django.http import HttpResponseRedirect 

from horizon import exceptions
from horizon import forms
from horizon import tables


from openstack_dashboard import api
from openstack_dashboard import get_ip
from openstack_dashboard.dashboards.project import Mysql



try:
    from django.utils.http import is_safe_url
except ImportError:
    from .utils import is_safe_url

from keystoneclient.v2_0 import client as keystone_client_v2
from keystoneclient import exceptions as keystone_exceptions

from .forms import Login
from .user import set_session_from_user, create_user_from_token, Token
from .utils import get_keystone_client
from .utils import get_keystone_version



#from openstack_dashboard.dashboards.admin.users \
#    import forms as project_forms
#from openstack_dashboard.dashboards.admin.users \
#    import tables as project_tables


LOG = logging.getLogger(__name__)


@sensitive_post_parameters()
@csrf_protect
@never_cache

#index3
#def index3(request):
 #   return render(request, 'auth/index3.html')



def login(request):
    """ Logs a user in using the :class:`~openstack_auth.forms.Login` form. """
    # Get our initial region for the form.
    initial = {}
    current_region = request.session.get('region_endpoint', None)
    requested_region = request.GET.get('region', None)
    regions = dict(getattr(settings, "AVAILABLE_REGIONS", []))
    if requested_region in regions and requested_region != current_region:
        initial.update({'region': requested_region})

    if request.method == "POST":
        form = curry(Login, request)
    else:
        form = curry(Login, initial=initial)

    extra_context = {'redirect_field_name': REDIRECT_FIELD_NAME}

    if request.is_ajax():
        template_name = 'auth/_login.html'
        extra_context['hide'] = True
    else:
        template_name = 'auth/login.html'

    res = django_login(request,
                       template_name=template_name,
                       authentication_form=form,
                       extra_context=extra_context)
    # Set the session data here because django's session key rotation
    # will erase it if we set it earlier.
    if request.user.is_authenticated():
        set_session_from_user(request, request.user)
        regions = dict(Login.get_region_choices())
        region = request.user.endpoint
        region_name = regions.get(region)
        request.session['region_endpoint'] = region
        request.session['region_name'] = region_name
    return res


def logout(request):
    msg = 'Logging out user "%(username)s".' % \
        {'username': request.user.username}
    LOG.info(msg)
    if 'token_list' in request.session:
        t = Thread(target=delete_all_tokens,
                   args=(list(request.session['token_list']),))
        t.start()
    """ Securely logs a user out. """
    return django_logout(request)


def delete_all_tokens(token_list):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    for token_tuple in token_list:
        try:
            endpoint = token_tuple[0]
            token = token_tuple[1]
            if get_keystone_version() < 3:
                client = keystone_client_v2.Client(endpoint=endpoint,
                                                token=token,
                                                insecure=insecure,
                                                debug=settings.DEBUG)
                client.tokens.delete(token=token)
            else:
                # FIXME: KS-client does not have delete token available
                # Need to add this later when it is exposed.
                pass
        except keystone_exceptions.ClientException as e:
            LOG.info('Could not delete token')


@login_required
def switch(request, tenant_id, redirect_field_name=REDIRECT_FIELD_NAME):
    """ Switches an authenticated user from one project to another. """
    LOG.debug('Switching to tenant %s for user "%s".'
              % (tenant_id, request.user.username))
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    endpoint = request.user.endpoint
    try:
        if get_keystone_version() >= 3:
            endpoint = endpoint.replace('v2.0', 'v3')

        client = get_keystone_client().Client(tenant_id=tenant_id,
                                              token=request.user.token.id,
                                              auth_url=endpoint,
                                              insecure=insecure,
                                              debug=settings.DEBUG)
        auth_ref = client.auth_ref
        msg = 'Project switch successful for user "%(username)s".' % \
            {'username': request.user.username}
        LOG.info(msg)
    except keystone_exceptions.ClientException:
        msg = 'Project switch failed for user "%(username)s".' % \
            {'username': request.user.username}
        LOG.warning(msg)
        auth_ref = None
        LOG.exception('An error occurred while switching sessions.')

    # Ensure the user-originating redirection url is safe.
    # Taken from django.contrib.auth.views.login()
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = settings.LOGIN_REDIRECT_URL

    if auth_ref:
        user = create_user_from_token(request, Token(auth_ref), endpoint)
        set_session_from_user(request, user)
    return shortcuts.redirect(redirect_to)


def switch_region(request, region_name,
                  redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Switches the non-identity services region that is being managed
    for the scoped project.
    """
    if region_name in request.user.available_services_regions:
        request.session['services_region'] = region_name
        LOG.debug('Switching services region to %s for user "%s".'
                  % (region_name, request.user.username))

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = settings.LOGIN_REDIRECT_URL

    return shortcuts.redirect(redirect_to)

@csrf_exempt
def register(request):
	
	errors= [] 
	username=None
	password=None
	password1=None
	email=None
	
	if request.method == 'POST':
		if not request.POST.get('username'):
			errors.append('Please Enter username')
		else:
			username = request.POST.get('username')
		if not request.POST.get('password'):
			errors.append('Please Enter password')
		else:
			password= request.POST.get('password')
		if not request.POST.get('password1'):
			errors.append('Please Enter confirmpassword')
		else:
			password1= request.POST.get('password1')  
		if not request.POST.get('email'):
                        errors.append('Please Enter email')
                else:
                        email = request.POST.get('email')
		
		if username and password and password1 and email:
			ut = create_user(username, password, email)
			#database test_zxl , table user
			sql = "insert into user(userid, account, username, password, tenantid) value ('%s', '%s', '%s', '%s', '%s')"%(ut.user_id, 0, username,password,ut.tenant_id)
			Mysql.insertData(sql)	
			return HttpResponseRedirect('/horizon/auth/login')			

	return render(request,"auth/register.html")


#add function --->  user registration



#def get_tenantid(userid):
class u_t:
	user_id = ''
	tenant_id = ''
	def __init__(self, u, t):
		self.user_id = u;
		self.tenant_id = t;
	

def create_user(username, password, email):
	ip = get_ip.get_one_ip('local_ip')
	url1="%s:5000" % (ip)
	params1 ='{"auth": {"tenantName": "admin","passwordCredentials": { "username": "admin","password": "cloud"}}}'
	headers1 = {"Content-Type": 'application/json'}
	conn1 = httplib.HTTPConnection(url1)
	conn1.request("POST","/v2.0/tokens",params1,headers1)
	response1 = conn1.getresponse()
	data1 = response1.read()
#token=response1.getheader('x-subject-token')
	dd1 = json.loads(data1)
	conn1.close()

	token= dd1['access']['token']['id']
	headers1 = {"X-Auth-Token":token,"Content-Type": 'application/json'}
	conn1 = httplib.HTTPConnection(url1)
#conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata)  
	info_project = '{"project": {"enabled": true,"name": "%s"}}'%(username)
	conn1.request("POST","/v3/projects",info_project,headers1)
	response1 = conn1.getresponse()
	data1 = response1.read()
	dd1 = json.loads(data1)
	conn1.close()
#print dd1
	pro_id = dd1['project']['id']
         
	info_role = '{"name": "Member"}' 
	conn1.request("GET","/v3/roles?name=Member","",headers1)
	response1 = conn1.getresponse()
	data1 = response1.read()
	dd1 = json.loads(data1)
	conn1.close()
#print dd1
	r_member_id = dd1['roles'][0]['id']
#print r_member_id
    
    
    
	info='{"user": {"default_project_id": "%s","email": "%s","enabled": 1,"name": "%s","password": "%s"}}' %(pro_id, email, username, password)
#print info
	conn1.request("POST","/v3/users",info,headers1)
	response1 = conn1.getresponse()
	data1 = response1.read()
	dd1 = json.loads(data1)
	conn1.close()
#print dd1

	user_id = dd1['user']['id']



	url_grant = '/v3/projects/%s/users/%s/roles/%s' %(pro_id, user_id, r_member_id)
#print url_grant
	conn1.request("PUT",url_grant,"",headers1)
#response1 = conn1.getresponse()  
#data1 = response1.read()
#dd1 = json.loads(data1)
	conn1.close()
#print dd1
	ut = u_t(user_id, pro_id)
	return ut

	





"""
class IndexView(tables.DataTableView):
    table_class = project_tables.UsersTable
    template_name = 'admin/users/index.html'

    def get_data(self):
        users = []
        domain_context = self.request.session.get('domain_context', None)
        try:
            users = api.keystone.user_list(self.request,
                                           domain=domain_context)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve user list.'))
        return users
"""


