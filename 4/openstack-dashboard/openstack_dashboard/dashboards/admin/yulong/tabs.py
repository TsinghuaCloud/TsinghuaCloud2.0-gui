from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tabs


class FlockingTab(tabs.Tab):
    name = _("TestTabs")
    slug = "TestTabs"
    template_name = ("admin/yulong/flock.html")
    #preload = False

    def get_context_data(self, request):
        context = {'yulong': 'tefd'}
        return context
class SecondFlockingTab(tabs.Tab):
    name = _("second")
    slug = "second"
    template_name = ("admin/yulong/second.html")
    #preload = False

    def get_context_data(self, request):
        context = {'yulong': 'second'}
        return context

class FlockingOverviewTabs(tabs.TabGroup):
    slug = "flocking_overview"
    tabs = (FlockingTab,SecondFlockingTab)
    sticky = True
