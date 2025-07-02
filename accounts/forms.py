from django import forms
from django.contrib.auth.forms import PasswordChangeForm

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