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

from datetime import datetime  # noqa
import pytz

from django.conf import settings  # noqa
from django import shortcuts
from django.utils import encoding
from django.utils import translation
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import forms
from horizon import messages

from openstack_dashboard.dashboards.project import Mysql

def update_user(money, userid):
	sql = "update user set account = account + '%s' where userid = '%s'"%(money, userid)
	Mysql.updateData(sql)

def insert_userinfo(money, userid):
	time = datetime.now()
	print "this is time :::'%s'" % time
	sql = "insert into user_info(userid, instanceid, op, money, time) value ('%s', '%s', '%s', '%s', '%s')" % (userid,'', '+', money, time)
	Mysql.insertData(sql) 	

class UserChargeForm(forms.SelfHandlingForm):
    
    charge_money = forms.CharField(label = _("Charge"))

    def __init__(self, *args, **kwargs):
        super(UserChargeForm, self).__init__(*args, **kwargs)
   


    def handle(self, request, data):
#        response = shortcuts.redirect(request.build_absolute_uri())
 	response = shortcuts.redirect('/horizon/costs/')      	 
	money = data['charge_money']
	userid = request.user.id
	print "this is usercharge reponse:::::'%s'" % response
	print "this is usercharge userid:::::'%s'" % userid
	print "this is usercharge money::::::::::::'%s'" % money	
	update_user(money, userid)
	insert_userinfo(money, userid)
	msg=_("charge success!")
	messages.success(request,msg) 	
	
        return response
