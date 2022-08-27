from django import forms
from django.contrib.auth.password_validation import password_changed
from django.forms import TextInput, PasswordInput, ValidationError
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class HappyShopTextInput(TextInput):
    input_type = "text"
    template_name = "happy_shop/widgets/text.html"


class HappyShopPasswordInput(PasswordInput):
    input_type = "password"
    template_name = "happy_shop/widgets/text.html"


class HappyShopLoginForm(AuthenticationForm):
    """ 登录表单 """
    username = UsernameField(
        widget=HappyShopTextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=HappyShopPasswordInput(
            attrs={"autocomplete": "current-password"}),
    )


class HappyShopRegisterForm(UserCreationForm):
    """ 注册视图 """
    
    password1 = forms.CharField(
        label=("密码"),
        strip=False,
        widget=HappyShopPasswordInput(attrs={"autocomplete": "new-password", }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("确认密码"),
        widget=HappyShopPasswordInput(attrs={"autocomplete": "new-password", }),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}
        widgets = {
            'username': HappyShopTextInput(attrs={"autofocus": True}),
        }
    
