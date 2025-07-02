from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):
    """整合Django认证系统的登录验证中间件"""
    
    def process_request(self, request):
        # 定义白名单：URL路径或URL名称（更推荐用名称）
        white_list = [
            reverse('login'),          # 登录页面
            reverse('image_code'),     # 验证码
            reverse('admin:index'),    # Django后台管理页面
            reverse('admin:login'), 
        ]
        
        # 1. 检查当前请求是否在白名单内
        if request.path_info in white_list:
            return
        # if any(request.path_info == url or request.path_info.startswith(url) for url in white_list):
        #     return
        
        # 2. 检查用户是否已通过Django认证系统登录
        if request.user.is_authenticated:
            return
        
        # 3. 未登录则重定向到登录页面，并传递当前URL作为next参数
        return redirect(f'/login/?next={request.path_info}')