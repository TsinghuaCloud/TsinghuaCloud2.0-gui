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

from django.core.urlresolvers import reverse_lazy  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import exceptions
from horizon import tables
from horizon import workflows

from openstack_dashboard import api

from openstack_dashboard.dashboards.admin.flavors \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.flavors \
    import workflows as flavor_workflows


from openstack_dashboard.dashboards.admin.flavors import Mysql

INDEX_URL = "horizon:admin:flavors:index"

def get_instance_type():
	sql = "select * from instance_types where deleted = 0"
	flavorss = Mysql.selectData(sql)
	return flavorss

def _dict_to_object(d):
    class O: pass
    for _k in d:
        if type(d[_k]) == dict:
            setattr(O, _k, Struct(**d[_k]))
        else:
            setattr(O, _k, d[_k])
    return O

def get_one_flavor(id):
	sql = "select * from instance_types where id = '%s'" % id
	flavor = Mysql.selectData(sql)
	return flavor


class IndexView(tables.DataTableView):
    table_class = project_tables.FlavorsTable
    template_name = 'admin/flavors/index.html'

    def get_data(self):
        request = self.request
        flavors = []
        try:
            # "is_public=None" will return all flavors.
    #        flavors = api.nova.flavor_list(request, None)
	    flavorsinfo = get_instance_type()
	    for i in range(len(flavorsinfo)):
		flavors.append(_dict_to_object(flavorsinfo[i]))
        except Exception:
            exceptions.handle(request,
                              _('Unable to retrieve flavor list.'))
        # Sort flavors by size
	
        flavors.sort(key=lambda f: (f.vcpus, f.memory_mb, f.root_gb))
	print "this is IndexView flavors: '%s'" % flavors
	for flavor in flavors:
		print "this is IndexView flavor::: '%s'" % flavor
#		print "this is IndexView flavor price::: '%s'" % flavor.price
        return flavors


class CreateView(workflows.WorkflowView):
    workflow_class = flavor_workflows.CreateFlavor
    template_name = 'admin/flavors/create.html'


class UpdateView(workflows.WorkflowView):
    workflow_class = flavor_workflows.UpdateFlavor
    template_name = 'admin/flavors/update.html'

    def get_initial(self):
        flavor_id = self.kwargs['id']
	print "this is flavor_id ::::: '%s'" % flavor_id

        try:
            # Get initial flavor information
#            flavor = api.nova.flavor_get(self.request, flavor_id)
	    flavor = get_one_flavor(flavor_id)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve flavor data.'),
                              redirect=reverse_lazy(INDEX_URL))
        return {'flavor_id': flavor[0]['flavorid'],
                'name': flavor[0]['name'],
                'vcpus': flavor[0]['vcpus'],
                'memory_mb': flavor[0]['memory_mb'],
                'disk_gb': flavor[0]['root_gb'],
               # 'swap_mb': flavor[0]['swap'] or 0,
               # 'eph_gb': getattr(flavor[0]['ephemeral_gb'], 'OS-FLV-EXT-DATA:ephemeral', None),
		'price': flavor[0]['price']}
