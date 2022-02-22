from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoreConfig(AppConfig):
    name = "project_express_till.store"
    verbose_name = _("Store")    
