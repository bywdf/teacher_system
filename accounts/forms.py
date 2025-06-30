from django import forms


class ImportUsersForm(forms.Form):
    excel_file = forms.FileField(label='选择Excel文件')
    
