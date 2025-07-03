from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import get_user_model
from django.core.validators import RegexValidator, validate_email
from accounts.models import Department, Subject, UserInfo

from accounts.models import UserInfo


class ImportUsersForm(forms.Form):
    excel_file = forms.FileField(label='选择Excel文件')




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="当前密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="确认新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    
class AvatarUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        label="选择头像",
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = UserInfo
        fields = ['avatar']
        
        
User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'gender', 'phone', 'email', 'idnumber',
            'nation', 'political_status', 'native_place', 'address', 
            'first_education', 'first_education_school', 'first_education_major', 'first_education_time',
            'highest_education', 'highest_education_school', 'highest_education_major', 'highest_education_time',
            'birthday', 'department', 'subject'
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'first_education_time': forms.DateInput(attrs={'type': 'date'}),
            'highest_education_time': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加字段样式
        self.fields['department'].queryset = Department.objects.all()
        self.fields['subject'].queryset = Subject.objects.all()
        self.fields['department'].empty_label = "请选择部门"
        self.fields['subject'].empty_label = "请选择学科"

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # 如果手机号为空，跳过验证
        if not phone:
            return phone
            
        # 手机号格式验证
        if not phone.isdigit() or len(phone) != 11:
            raise forms.ValidationError("请输入11位有效的手机号码")
        # 唯一性验证
        if UserInfo.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("该手机号已被使用")
        return phone

    def clean_idnumber(self):
        idnumber = self.cleaned_data['idnumber']
        # 如果身份证号为空，跳过验证
        if not idnumber:
            return idnumber
            
        # 身份证格式验证
        if len(idnumber) not in (15, 18) or not (idnumber[:-1].isdigit() and (idnumber[-1].isdigit() or idnumber[-1] in 'Xx')):
            raise forms.ValidationError("请输入有效的身份证号码")
        # 唯一性验证
        if UserInfo.objects.filter(idnumber=idnumber).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("该身份证号已被使用")
        return idnumber

    def clean_email(self):
        email = self.cleaned_data['email']
        # 如果邮箱为空，跳过验证
        if not email:
            return email
            
        # 邮箱格式验证
        try:
            validate_email(email)
        except:
            raise forms.ValidationError("请输入有效的邮箱地址")
        # 唯一性验证
        if UserInfo.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("该邮箱已被使用")
        return email