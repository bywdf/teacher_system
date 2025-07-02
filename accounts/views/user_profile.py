# accounts/views.py
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

#@login_required(login_url='login') 已经中间件控制登录状态了，装饰器在精细权限管理时才使用
def user_profile(request):
    """用户个人信息展示页"""
    user = request.user
    context = {
        'user': user,
        'page_title': '个人资料',
        'section': 'profile',
    }
    return render(request, 'profile.html', context)