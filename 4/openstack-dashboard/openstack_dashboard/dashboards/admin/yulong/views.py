from horizon import tabs

from openstack_dashboard.dashboards.admin.yulong import tabs as lyltest_tabs
class IndexView(tabs.TabbedTableView):
    tab_group_class = lyltest_tabs.FlockingOverviewTabs
    template_name = 'admin/yulong/index.html'
