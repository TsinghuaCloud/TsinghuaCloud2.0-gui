# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 NEC Corporation
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
import logging

from django.core.urlresolvers import reverse  # noqa
from django import template
from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import tables

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class CostsTable(tables.DataTable):
    instance_id = tables.Column("instanceid",
                         verbose_name=_("Instance_Id"))
    instance_name = tables.Column("instancename",
			   verbose_name=_("Instance_Name"))
    op = tables.Column("op",
                       verbose_name=_("op"),)
    money = tables.Column("money", verbose_name=_("money"))
    time = tables.Column("time", verbose_name=_("time"))
   

    class Meta:
        name = "costs"
        verbose_name = _("Costs")
#        table_actions = (CreateNetwork, DeleteNetwork)
#        row_actions = (EditNetwork, CreateSubnet, DeleteNetwork)
