
from accounts import models
from django import forms
from django.core.validators import RegexValidator   # 引入正则
from django.core.exceptions import ValidationError  # 引入报错

from utils.bootstrap import BootStrapModelForm


# 用modelform，先写一个类
class UserModelForm(BootStrapModelForm):
    # 设置最小长度
    name = forms.CharField(min_length=2, label='用户名') 
    class Meta:
        model = models.UserInfo
        # fields = ['name', 'password', 'age', 'account', 'gender','creat_time', 'depart']
        fields = '__all__'  #  直接获取所有字段
        # widgets = {
        #     'name': forms.TextInput(attrs={'class':'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class':'form-control'}),
        # }
            
            

class UserModelForm(BootStrapModelForm):
    # 验证方式一：
    phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    
    class Meta:
        model = models.UserInfo
        # exclude = ['level']  这个是排除哪个字段
        fields = '__all__'

    # 验证方式二   clean_phone 自动生成的字段
    # 钩子方法 比如检验存在不存在，正则表达式都可以
    def clean_phone(self):
        txt_molile = self.cleaned_data["phone"]  # 用户输入的字段
        exists = models.UserInfo.objects.filter(phone=txt_molile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        else:
            return txt_molile   


class UserEditModelForm(BootStrapModelForm):
    
    phone = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    
    # phone = forms.CharField(disabled=True, label='手机号') #不让修改显示
    class Meta:
        model = models.UserInfo
        fields = ['phone', 'price', 'level', 'status']

    def clean_phone(self):
        
        # 当前编辑行的id:self.instance.pk 
        
        txt_molile = self.cleaned_data["phone"]  # 用户输入的字段
        # 排除自己以外的是不是存在
        exists = models.UserInfo.objects.exclude(id=self.instance.pk).filter(phone=txt_molile).exists()    
        if exists:
            raise ValidationError('手机号已存在')
        else:
            return txt_molile     
              