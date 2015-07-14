from django.utils.translation import ugettext_lazy as _  # noqa

import horizon
from openstack_dashboard.dashboards.admin import dashboard



class Yulong(horizon.Panel):
    name = _("Yulong")
    slug = 'yulong'
#    permissions = ('openstack.roles.admin',)


dashboard.Admin.register(Yulong)
