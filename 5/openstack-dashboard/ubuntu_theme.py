# The presence of this file in /etc/openstack-dashboard/ and/or
# /usr/share/openstack-dashboard/openstack_dashboard/local/ will
# enable the Ubuntu theme for Horizon.  To disable, remove the
# openstack-dashboard-ubuntu-theme package, or remove this file.
TEMPLATE_DIRS = ('/usr/share/openstack-dashboard-ubuntu-theme/templates', )

# Enable a panel in the Settings dashboard to allow generation of Juju
# environment configuration.
ENABLE_JUJU_PANEL = True
