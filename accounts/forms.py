from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from accounts.models import UserInfo


class ImportUsersForm(forms.Form):
    excel_file = forms.FileField(label='选择Excel文件')




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="当前密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '请输入当前密码',
        }
    )
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'password_too_short': '密码至少需要%(min_length)d个字符',
            'password_too_common': '密码太常见，容易被猜出',
            'password_entirely_numeric': '密码不能全为数字',
        },
        help_text="至少8位字符，包含字母和数字"
    )
    new_password2 = forms.CharField(
        label="确认新密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'password_mismatch': '两次输入的密码不一致',
        }
    )

    # 添加自定义验证方法
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        
        # 长度验证
        if len(password1) < 8:
            raise forms.ValidationError("密码至少需要8个字符")
        
        # 全数字验证
        if password1.isdigit():
            raise forms.ValidationError("密码不能全为数字")
            
        # 常见密码验证
        common_passwords = ["password", "12345678", "qwertyui"]
        if password1.lower() in common_passwords:
            raise forms.ValidationError("密码太常见，请使用更复杂的密码")
        
        return password1
    
    
class AvatarUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(
        label="选择头像",
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = UserInfo
        fields = ['avatar']