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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.conf import settings  # noqa
from horizon import forms
from horizon import tables
from horizon import exceptions
from openstack_dashboard import usage
from openstack_dashboard.usage import base 
#from openstack_dashboard.dashboards.settings.user import forms as user_forms
from openstack_dashboard.dashboards.costs.overview \
    import tables as costall_tables
from openstack_dashboard.dashboards.project import Mysql  

def query_info(userid):
	sql = "select * from user_info where userid = '%s'" % (userid)
	userinfo = Mysql.selectData(sql)
	return userinfo


def _dict_to_object(d):
    class O: pass
    for _k in d:
        if type(d[_k]) == dict:
            setattr(O, _k, Struct(**d[_k]))
        else:
            setattr(O, _k, d[_k])
    return O

def get_account(userid):
        sql = "select account from user where userid = '%s'" % (userid)
        account = Mysql.selectData(sql)
        #print account[0]['account']
        totalmoney =  account[0]['account']
        return totalmoney



class CostallView(tables.DataTableView):
    table_class = costall_tables.CostsTable
    account = 0
    template_name = 'costs/overview/index.html'
#    usage_class = usage.ProjectUsage
    def get_account(self):
	user_id = self.request.user.id
	print "CostallView::::::'%s'" % user_id 
	self.account = get_account(user_id)
	print "this is self.account '%s' " % self.account

 		
    def get_data(self): 
	try:
       	    self.get_account()
	    user_id = self.request.user.id
	   # print "CostallView::::::'%s'" % user_id
	    userinfo = query_info(user_id)
	    print  userinfo
            res=[]
            for  i in range(len(userinfo)):
                 res.append(_dict_to_object(userinfo[i]))
	    #print  userinfo[0][3]
           # print res
	    #print  userinfo['op']
	    print "this is res '%s'" % res 
	except Exception: 
	    userinfo = [] 
            msg = _('userinfo list can not be retrieved.')
	    #msg = ('userinfo list can not be retrieved.') 
            exceptions.handle(self.request, msg)  
	    
	return res

