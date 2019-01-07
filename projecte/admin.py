from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


class ProjectEAdminSite(AdminSite):
    site_title = ugettext_lazy('ProjectE admin')
    site_header = ugettext_lazy('ProjectE administration')
    index_title = ugettext_lazy('ProjectE administration')


admin = ProjectEAdminSite()
