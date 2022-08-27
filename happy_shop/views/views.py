from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, View, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
# Create your views here.
from happy_shop.models import HappyShopingCart, HappyShopCategory
from happy_shop.conf import happy_shop_settings
from happy_shop.utils import add_upload_file
from happy_shop.forms import HappyShopLoginForm, HappyShopRegisterForm


class BaseView:
    """全局基类视图"""
    
    title = happy_shop_settings.TITLE
    desc = happy_shop_settings.DESC
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['desc'] = self.desc
        if self.request.user.is_authenticated:
            context['cart_num'] = HappyShopingCart.get_cart_count(self.request.user)
        else:
            context['cart_num'] = 0
        return context


class HappyShopLoginRequiredMixin(LoginRequiredMixin):
    """ 
    全局登陆校验 
    """
    login_url = 'happy_shop:login'
    redirect_field_name = 'redirect_to'


class HappyShopLoginView(BaseView, LoginView):
    """
    登录视图
    """
    form_class = HappyShopLoginForm
    template_name = "happy_shop/login.html"
    next_page = "happy_shop:index"
    extra_context = {
        "site_title": "登录",
    }


class HappyShopRegisterView(SuccessMessageMixin, BaseView, FormView):
    """
    注册用户 
    """
    template_name = 'happy_shop/register.html'
    form_class = HappyShopRegisterForm
    success_url = reverse_lazy("happy_shop:index")
    success_message = "%(username)s 注册成功，已登录！"
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(username=new_user.username, 
                                     password=form.cleaned_data['password1'])
            # UserProfile.objects.create(user=auth_user)
            login(self.request, auth_user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )


class HappyShopLogoutView(BaseView, LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """


class HappyShopUploadImage(LoginRequiredMixin, View):
    """富文本编辑器上传图片
    首先会检查项目根目录有没有media/upload/的文件夹
    如果没有就创建，图片最终保存在media/upload/目录下
    返回图片路径为 "/media/upload/file.png"
    wangEditor_v4文档：https://www.wangeditor.com/
    """
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # 无登录后台管理权限的用户不能上传
        if not request.user.is_staff:
            return JsonResponse({"errno": 1,"data":[]})
        
        # 返回数据中需要的data
        data = []
        file_data = request.FILES
        keys = list(file_data.keys())
        for key in keys:
            img_dict = {}
            file = file_data.get(f'{key}')
            # 上传
            add_upload_file(file)
            # 构造返回数据
            img_dict['url'] = f'/{happy_shop_settings.FILE_PATH}{file.name}'
            data.append(img_dict) 
        context = {"errno": 0,"data":data}
        return JsonResponse(context)


class HappyShopCategoryAllView(BaseView, TemplateView):
    """ 所有分类
    """
    template_name = 'happy_shop/categorys.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navs"] = HappyShopCategory.get_navs()
        return context
    
    
    