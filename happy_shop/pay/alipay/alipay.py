"""支付宝支付初始化

这里用到了第三方的支付SDK，感谢作者的辛勤付出！
Github: https://github.com/fzlee/alipay
Docs:   https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
"""

from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig

from happy_shop.conf import happy_shop_settings

private_path = happy_shop_settings.ALIPAY.get('PRIVATE_KEY')
public_path = happy_shop_settings.ALIPAY.get('PUBLIC_KEY')

app_private_key_string = open(private_path).read()
alipay_public_key_string = open(public_path).read()

app_private_key_string == """
    -----BEGIN RSA PRIVATE KEY-----
    base64 encoded content
    -----END RSA PRIVATE KEY-----
"""

alipay_public_key_string == """
    -----BEGIN PUBLIC KEY-----
    base64 encoded content
    -----END PUBLIC KEY-----
"""

alipay = AliPay(
    appid=happy_shop_settings.ALIPAY.get('APPID'),
    app_notify_url=happy_shop_settings.ALIPAY.get('NOTIFY_URL'),  # 默认回调 url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=happy_shop_settings.ALIPAY.get('DEBUG'),  # 默认 False
    # verbose=happy_shop_settings.ALIPAY.get('DEBUG'),  # 输出调试数据
    verbose=False,
    config=AliPayConfig(timeout=15)  # 可选，请求超时时间
)

# dc_alipay = DCAliPay(
#     appid="appid",
#     app_notify_url="http://example.com/app_notify_url",
#     app_private_key_string=app_private_key_string,
#     app_public_key_cert_string=app_public_key_cert_string,
#     alipay_public_key_cert_string=alipay_public_key_cert_string,
#     alipay_root_cert_string=alipay_root_cert_string
# )

# 如果您没有听说过 ISV， 那么以下部分不用看了
# app_auth_code 或 app_auth_token 二者需要填入一个
# isv_alipay = ISVAliPay(
#     appid="",
#     app_notify_url=None,  # 默认回调 url
#     app_private_key_srting="",
#     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#     alipay_public_key_string="",
#     sign_type="RSA",  # RSA or RSA2
#     debug=False,  # False by default
#     app_auth_code=None,
#     app_auth_token=None
# )