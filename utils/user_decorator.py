from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from functools import wraps

from django.shortcuts import render


def admin_or_superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # 检查是否为超级管理员或属于"管理员组"
        is_admin = user.is_superuser or (
            user.is_authenticated and 
            user.groups.filter(name="管理员").exists()
        )
        
        if not is_admin:
            return HttpResponseForbidden("您没有权限访问")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
# @admin_or_superuser_required

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            # 渲染no_permission.html模板并返回403状态码
            return render(request, 'no_permission.html', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view