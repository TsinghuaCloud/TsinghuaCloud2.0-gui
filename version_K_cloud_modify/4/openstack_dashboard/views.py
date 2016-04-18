# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import json
import get_ip
from django.http import HttpResponseRedirect
from django import shortcuts
import django.views.decorators.vary
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

import horizon
from horizon import base
from horizon import exceptions
from django.http import HttpResponse
from openstack_auth import views
#from openstack_dashboard.dashboards.admin.flavors import Mysql


def get_user_home(user):
    dashboard = None
    if user.is_superuser:
        try:
            dashboard = horizon.get_dashboard('admin')
        except base.NotRegistered:
            pass

    if dashboard is None:
        dashboard = horizon.get_default_dashboard()

    return dashboard.get_absolute_url()


@django.views.decorators.vary.vary_on_cookie
#def splash(request):
#    if not request.user.is_authenticated():
#        raise exceptions.NotAuthenticated()
#
#    response = shortcuts.redirect(horizon.get_user_home(request.user))
#    if 'logout_reason' in request.COOKIES:
#        response.delete_cookie('logout_reason')
#    return response

def splash(request):
    if request.user.is_authenticated():
#	print "faksjflkdasjoif: request.META['HTTP_REFERER'] :'%s'" % request.META['HTTP_REFERER']

	if len(request.META['HTTP_REFERER']) > 36 :
		print "thisis if"
		t = request.META['HTTP_REFERER']
		l = len(t)
		print request.META['HTTP_REFERER']
		print "this is l: '%s'" % l
		tt = t[l-1]
		print "this is tt: '%s'" % tt
		if tt == '1' :
			return shortcuts.redirect(get_user_home(request.user))
		elif tt == '3' and request.user.is_superuser :
			ip = get_ip.get_one_ip('homepage_ip')
			url = 'http://%s/hoststatus' % (ip)
			return HttpResponseRedirect(url)
	else:
		return shortcuts.redirect(get_user_home(request.user))
#       return shortcuts.render(request, "admin")
    if request.GET.has_key('from_where'):
    	tt =  request.GET['from_where']
    	form = views.Login(request)
    	request.session.clear()
    	request.session.set_test_cookie()
    	return shortcuts.render(request, 'splash.html', {'form': form, 'tt': tt})
    else:
	form = views.Login(request)
	request.session.clear()
	request.session.set_test_cookie()
	return shortcuts.render(request, 'splash.html', {'form': form})
