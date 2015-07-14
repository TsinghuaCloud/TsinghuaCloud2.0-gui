# vim: tabstop=4 shiftwidth=4 softtabstop=4

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
from django.views.decorators import vary
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import horizon
from django.http import HttpResponse
from openstack_auth import views
from openstack_dashboard.dashboards.admin.flavors import Mysql
#huoqu yonghuming , panduan yonghu quanxian ,yongyu shezhi tiaozhuanjiemian

@csrf_exempt
def getprice(request):
    print "this is ajax getprice!!"
    print "this is request:: '%s' " % request
    if request.GET.has_key('flavorid'):
        flavor_id = request.GET['flavorid']
        result = {}
        sql = "select price from instance_types where flavorid = '%s' and deleted = '0'" % flavor_id
        info = Mysql.selectData(sql)
        result['price'] = info[0]['price']
        return HttpResponse(json.dumps(result), content_type = "application/json")
    else:
        print "not get request!"

def get_user_home(user):
    if user.is_superuser:
        return horizon.get_dashboard('admin').get_absolute_url()
    return horizon.get_dashboard('project').get_absolute_url()


@vary.vary_on_cookie
#huoqu denglu jiemian de yonghuming he mima , yanzheng tongguo ze panduan yonghuquanxian, fouze shuaxin
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

def index(request):
    return render(request,'index.html')
