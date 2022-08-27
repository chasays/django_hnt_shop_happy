from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from ..forms import HappyShopTextInput, HappyShopPasswordInput


class HappyShopAdminAuthenticationForm(AdminAuthenticationForm):
    """后台登录表单
    """
    username = UsernameField(widget=HappyShopTextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=HappyShopPasswordInput(attrs={"autocomplete": "current-password"}),
    )