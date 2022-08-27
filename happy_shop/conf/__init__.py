"""
SimpleShop框架的设置都在 HAPPY_SHOP 设置中命名。
例如，您项目的 `settings.py` 文件可能如下所示：

HAPPY_SHOP = {
    'ALIPAY':{
        'APPID': '2021000116697536',
        'RETURN_URL': 'http://mall.lotdoc.cn/happy/api/alipay/',
        'NOTIFY_URL': 'http://mall.lotdoc.cn/happy/api/alipay/',
        'DEBUG': DEBUG,           # 开发模式默认为True，部署时设置为False
        'PRIVATE_KEY':BASE_DIR / 'happy_shop/pay/alipay/keys/app_private_key.pem',
        'PUBLIC_KEY':BASE_DIR / 'happy_shop/pay/alipay/keys/app_public_key.pem',
    },
}

该模块提供了 `happy_shop_settings` 对象，用于访问 HAPPY_SHOP设置，
先检查用户设置，然后下降回到默认值。

This module provides the `simple_shop_settings` object, that is used to access
REST framework settings, checking for user settings first, then falling
back to the defaults.
"""

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string
from .default_settings import DEFAULTS, IMPORT_STRINGS, REMOVED_SETTINGS


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class APISettings:
    """
    一个设置对象，允许 SIMPLE_SHOP 设置在项目中随意加载。 
    例如需要引用配置中的项，如下：

        from happy_shop.conf import happy_shop_settings
        print(happy_shop_settings.TITLE)

    任何带有字符串导入路径的设置都会被自动解析并返回类，而不是字符串文字。

    备注：
    这是一个仅与命名空间设置兼容的内部类在 HAPPY_SHOP 名称下。
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'HAPPY_SHOP', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "#"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError("The '%s' setting has been removed. Please refer to '%s' for available settings." % (setting, SETTINGS_DOC))
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


happy_shop_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_happy_shop_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'HAPPY_SHOP':
        happy_shop_settings.reload()


setting_changed.connect(reload_happy_shop_settings)