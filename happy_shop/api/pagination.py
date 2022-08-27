from rest_framework.pagination import PageNumberPagination
from happy_shop.conf import happy_shop_settings


class HappyShopSKUPagination(PageNumberPagination):
    """ 商品分页 """
    page_size = happy_shop_settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = happy_shop_settings.MAX_PAGE_SIZE
    