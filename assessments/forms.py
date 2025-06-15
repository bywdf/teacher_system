# forms.py
from django import forms
from django.core.validators import FileExtensionValidator

# forms.py
class BatchImportForm(forms.Form):
    excel_file = forms.FileField(
        label="上传 Excel 文件",
        validators=[FileExtensionValidator(allowed_extensions=['xlsx'])],
    )