from django.conf import settings  # noqa
from django.http import HttpResponse  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api
from openstack_dashboard.usage import quotas

from openstack_dashboard.dashboards.project import Mysql

def get_account(userid):
        sql = "select account from user where userid = '%s'" % (userid)
        account = Mysql.selectData(sql)
        #print account[0]['account']
        totalmoney =  account[0]['account']
        return totalmoney

class Use(object):
    show_terminated = False

    def __init__(self, request, project_id=None):
        self.project_id = project_id or request.user.tenant_id
        self.user_id = request.user.id
        self.request = request
        self.account = 0
    def get_account(self):
        self.account = get_account(self.user_id)
        print "this use account: '%s'" % self.account
	
