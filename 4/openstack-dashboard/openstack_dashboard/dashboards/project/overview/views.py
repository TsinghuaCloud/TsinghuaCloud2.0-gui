# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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


from django.template.defaultfilters import capfirst  # noqa
from django.template.defaultfilters import floatformat  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa
from django.views.generic import TemplateView  # noqa

from openstack_dashboard import usage
from openstack_dashboard.usage import base
from openstack_dashboard.dashboards.project import Mysql

class ProjectUsageCsvRenderer(base.BaseCsvResponse):

    columns = [_("Instance Name"), _("VCPUs"), _("Ram (MB)"),
               _("Disk (GB)"), _("Usage (Hours)"),
               _("Uptime(Seconds)"), _("State")]

    def get_row_data(self):

        for inst in self.context['usage'].get_instances():
            yield (inst['name'],
                   inst['vcpus'],
                   inst['memory_mb'],
                   inst['local_gb'],
                   floatformat(inst['hours'], 2),
                   inst['uptime'],
                   capfirst(inst['state']))

def get_account(userid): 
#	userid = get_userid()
	print userid
	sql = "select account from user where userid = '%s'" % (userid)
	account = Mysql.selectData(sql)
	print account 
	totalmoney =  account[0][0] 
	return totalmoney

class ProjectOverview(usage.UsageView):
    table_class = usage.ProjectUsageTable
    usage_class = usage.ProjectUsage
   
    template_name = 'project/overview/usage.html'
    csv_response_class = ProjectUsageCsvRenderer
    #print self.request.user.idi
#    print account   

    def get_data(self):
        #print self.session.user.id
	super(ProjectOverview, self).get_data()
#	userid =  self.request.user.id
#	account = get_account(userid)
#	print "this is account : '%s'" % account
	print "this overview usage.account '%s'" % self.usage.account
        return self.usage.get_instances()
    
# zxl: get attr account:
'''
    def get_userid(self):
	super(ProjectOverview, self).get_data() 
	userid = self.request.user.id
	print userid 
	return userid

    print get_account(get_userid)
'''


class WarningView(TemplateView):
    template_name = "project/_warning.html"

#def query_account():
#	sql = "se"
