from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



from accounts import models
from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm
from utils.encrypt import md5



def user_list(request):
    """用户列表"""
    
    # info_dict = request.session['info'] 获取登录信息
    # info_dict[id]
    
    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict['name__contains']= search_data 
    
    # 根据搜索条件去数据库获取
    queryset = models.User.objects.filter(**data_dict)
    
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset,     # 分页数据
        'page_string': page_object.html(),         # 生成页码
    }

    return render(request, 'user_list.html', context)


class UserModelForm(BootStrapModelForm):
    
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
        )
    
    class Meta:
        model = models.User
        fields = ['username', 'name', 'gender', 'phone', 'email', 'idnumber', 'department', 'subject', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("两次输入的密码不一致")
        return confirm  # 返回什么。此字段就保存此数据库


def user_add(request):
    """添加用户"""
    
    title = '新建用户'
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')
    
    return render(request, 'change.html', {'form': form, 'title': title})


class UserEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = ['username']


def user_edit(request, nid):
    """编辑用户"""
    # 对象 / None
    title = '编辑用户'
    row_object = models.User.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html', {"msg":"数据不存在"})

    # 要是单独只能修改某几个字段，单独写一个form类
    if request.method == 'GET':
        form = UserEditModelForm(instance=row_object) 
        return render(request, 'change.html', {'form':form, 'title': title})
    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


def user_delete(request, nid):
    """删除用户"""
    models.User.objects.filter(id=nid).delete()
    return redirect('/user/list/')


class UserRestModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
        )
    
    class Meta:
        model = models.User
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }  
        
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        
        # 去数据库校验新输入的密码和之前的密码是否是一样的
        exists = models.User.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前的相同')
        return md5(pwd)
    
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd and pwd!=None:
            raise ValidationError("两次输入的密码不一致")
        return confirm  # 返回什么。此字段就保存此数据库


def user_reset(request, nid):
    """重置密码"""
   
    row_object = models.User.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html', {"msg":"数据不存在"})
    
    title = '重置密码 - {}'.format(row_object.username)
    if request.method == 'GET':
        form =  UserRestModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    
    form =  UserRestModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, 'change.html', {'form': form, 'title': title})