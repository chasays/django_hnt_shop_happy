from pathlib import Path
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

alipay_private_key = BASE_DIR / 'pay/alipay/keys/app_private_key.pem'
alipay_public_key = BASE_DIR / 'pay/alipay/keys/app_public_key.pem'

DEFAULTS = {
    'TITLE': 'Helium',
    'DESC': '',

    # 支付宝支付的key文件路径
    'ALIPAY':{
        'APPID': '2021000116697536',
        'RETURN_URL': 'http://127.0.0.1:8000/shop/api/alipay/',
        'NOTIFY_URL': 'http://127.0.0.1:8000/shop/api/alipay/',
        'DEBUG': False,           # 开发模式默认为True，部署时设置为False
        'PRIVATE_KEY':alipay_private_key,
        'PUBLIC_KEY':alipay_public_key,
    },

    # 首页楼层商品显示数量
    'FLOOR_NUM': 8, 
    
    # 商品列表页分页
    'PAGE_SIZE': 20,       # 每页商品数量
    'MAX_PAGE_SIZE': 100,  # 最大分页数

    # 商品详情页新品推荐数量
    'NEW_NUM': 5,
    
    # 个人中心全部订单分页显示数量
    'ORDERS_NUM': 10,
    
    # 富文本编辑器上传保存图片路径
    'FILE_PATH': 'media/upload/',
    
    # ADMIN LOGO页配置
    'TITLE': 'Helium',
    'DESC': '',
    'LOGO': ''
        
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ],
}

# 可能采用字符串导入表示法的设置列表。
IMPORT_STRINGS = [
    'DEFAULT_RENDERER_CLASSES',
]

# 已删除的设置列表
REMOVED_SETTINGS = [
    'PAGINATE_BY', 'PAGINATE_BY_PARAM', 'MAX_PAGINATE_BY',
]
