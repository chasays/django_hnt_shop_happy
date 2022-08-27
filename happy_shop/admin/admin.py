from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy
from django.urls import reverse_lazy
from happy_shop.conf import happy_shop_settings
from .forms import HappyShopAdminAuthenticationForm


class HappyShopAdminSite(AdminSite):
    """自定义AdminSite
    """
    site_header = gettext_lazy("Helium Admin")
    site_title = gettext_lazy("Helium 后台管理")
    index_title = gettext_lazy("Helium admin")
    site_url = reverse_lazy("happy_shop:index")
    
    # index_template = "happy_shop/admin/index.html"
    
    login_form = HappyShopAdminAuthenticationForm
    login_template = "happy_shop/admin/login.html"
     
    def login(self, request, extra_context=None):
        extra_context = {
            'title': happy_shop_settings.TITLE,
            'desc': happy_shop_settings.DESC,
            'logo': happy_shop_settings.LOGO
        }
        return super().login(request, extra_context)
    
    def index(self, request, extra_context=None):
        extra_context = {
            'num':'num'
        }
        print(extra_context)
        return super().index(request, extra_context)
    
    
happy_shop_site = HappyShopAdminSite(name='happy_shop_admin')
