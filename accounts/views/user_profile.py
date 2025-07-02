# accounts/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from accounts.forms import CustomPasswordChangeForm, AvatarUpdateForm


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


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # 更新会话认证哈希，防止用户被注销
            update_session_auth_hash(request, form.user)
            messages.success(request, '密码修改成功！')
            return redirect('accounts:user_profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form})

def update_avatar(request):
    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '头像更新成功！')
            return redirect('accounts:user_profile')
    else:
        form = AvatarUpdateForm(instance=request.user)
    
    return render(request, 'update_avatar.html', {'form': form})