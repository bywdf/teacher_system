# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from accounts.forms import CustomPasswordChangeForm, AvatarUpdateForm, UserEditForm
from accounts.models import  UserInfo


#@login_required(login_url='login') 已经中间件控制登录状态了，装饰器在精细权限管理时才使用
# def user_profile(request):
#     """用户个人信息展示页"""
#     user = request.user
#     context = {
#         'user': user,
#         'page_title': '个人资料',
#         'section': 'profile',
#     }
#     return render(request, 'profile.html', context)
@login_required(login_url='login')
def user_profile(request):
    """用户个人信息展示页"""
    user_id = request.GET.get('user_id')
    
    # 检查用户是否属于校长组
    is_principal = request.user.groups.filter(name='管理员').exists()
    
    # 非校长组用户只能查看自己的信息
    if user_id and not is_principal:
        messages.error(request, "您没有权限查看其他用户的信息")
        return redirect('accounts:user_profile')  # 重定向到自己的信息页
    
    # 校长组用户可以查看任意用户信息
    if user_id and is_principal or request.user.is_superuser:
        try:
            user = UserInfo.objects.get(id=user_id)
            is_other_user = True
        except UserInfo.DoesNotExist:
            messages.error(request, "用户不存在")
            return redirect('accounts:user_list')  # 重定向到用户列表页
    else:
        # 普通用户或未提供user_id时查看自己的信息
        user = request.user
        is_other_user = False

    context = {
        'user': user,
        'page_title': '个人资料',
        'section': 'profile',
        'is_other_user': is_other_user,
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
            # 添加表单错误到消息
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AvatarUpdateForm(instance=request.user)
    
    return render(request, 'update_avatar.html', {'form': form})


def user_edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            # 更新用户名（手机号）
            new_phone = form.cleaned_data['phone']
            if new_phone != user.username:
                user.username = new_phone
                user.save(update_fields=['username'])
            
            # 保存表单数据
            form.save()
            messages.success(request, '资料更新成功！')
            return redirect('accounts:user_profile')
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
        'page_title': '编辑资料',
    }
    return render(request, 'user_edit_profile.html', context)