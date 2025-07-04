from io import BytesIO
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from utils.bootstrap import BootStrapForm
from utils.code import check_code

def index(request):
    return render(request, 'base.html')


def image_code(request):
    '''生成验证码'''

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中，以便后续获取验证码再进行校验
    request.session['image_code'] = code_string
    # 给Session设置一个60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())



class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        required=True,
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    
    # 移除原有的clean_password等验证方法，仅保留验证码验证
    def clean_code(self):
        user_input_code = self.cleaned_data.get('code')
        image_code = self.request.session.get('image_code', '')
        if not image_code:
            raise forms.ValidationError("验证码已过期")
        if image_code.lower() != user_input_code.lower():
            raise forms.ValidationError("验证码错误")
        return user_input_code
   

def user_login(request):
    """使用Django内置认证系统的登录功能"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    form = LoginForm(request.POST)
    form.request = request  # 将request传递给表单，以便验证验证码
    
    if form.is_valid():
        # 验证成功，获取用户名和密码
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # 使用Django内置认证函数验证用户
        user = authenticate(request, username=username, password=password)
        if not user:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        
        # 登录用户并设置会话
        login(request, user)
        request.session.set_expiry(60*60*24*7)  # 7天过期
        
        # 登录成功后重定向
        return redirect("index")
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    """用户登出"""
    logout(request)
    return redirect('login')