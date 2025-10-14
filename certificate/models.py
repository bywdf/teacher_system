from django.db import models
from django.conf import settings
import os
from django.core.validators import FileExtensionValidator

# 证书级别选择
CERTIFICATE_LEVELS = [
    ('county', '县级'),
    ('city', '市级'),
    ('province', '省级'),
    ('national', '国家级'),
]

# 文件上传路径函数
def certificate_upload_path(instance, filename):
    # 根据证书类型和教师ID组织文件路径
    if hasattr(instance, 'school_certificate'):
        cert_type = 'school'
        cert_id = instance.school_certificate.id
    else:
        cert_type = 'external'
        cert_id = instance.external_certificate.id
        
    # 添加时间戳以确保文件名唯一
    timestamp = instance.obtain_date.strftime('%Y%m%d')
    name, extension = os.path.splitext(filename)
    return f'certificates/{cert_type}/teacher_{instance.teacher.id}/{timestamp}_{cert_id}{extension}'


# 校级证书模型
class SchoolCertificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="证书名称")
    description = models.TextField(blank=True, verbose_name="证书描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    
    class Meta:
        verbose_name = "校级证书"
        verbose_name_plural = "校级证书"
        ordering = ['name']
        
    def __str__(self):
        return self.name


# 校外证书模型
class ExternalCertificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="证书名称")
    level = models.CharField(max_length=20, choices=CERTIFICATE_LEVELS, verbose_name="证书级别")
    description = models.TextField(blank=True, verbose_name="证书描述")
    issuing_authority = models.CharField(max_length=200, verbose_name="颁发机构")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    
    class Meta:
        verbose_name = "校外证书"
        verbose_name_plural = "校外证书"
        ordering = ['level', 'name']
        
    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"


# 教师获得校级证书模型
class TeacherSchoolCertificate(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='school_certificates',
        verbose_name="教师"
    )
    school_certificate = models.ForeignKey(
        SchoolCertificate, 
        on_delete=models.CASCADE, 
        verbose_name="校级证书"
    )
    obtain_date = models.DateField(verbose_name="获得时间")
    certificate_file = models.FileField(
        upload_to=certificate_upload_path,
        verbose_name="证书文件",
        help_text="支持图片(JPG, PNG)或PDF格式",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])],
        blank=True, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    notes = models.TextField(blank=True, verbose_name="备注")
    
    class Meta:
        verbose_name = "教师校级证书"
        verbose_name_plural = "教师校级证书"
        ordering = ['-obtain_date']
        
    def __str__(self):
        return f"{self.teacher} - {self.school_certificate} ({self.obtain_date.year})"
    
    def file_extension(self):
        name, extension = os.path.splitext(self.certificate_file.name)
        return extension.lower()
    
    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        return self.file_extension() in image_extensions
    
    def is_pdf(self):
        return self.file_extension() == '.pdf'


# 教师获得校外证书模型
class TeacherExternalCertificate(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='external_certificates',
        verbose_name="教师"
    )
    external_certificate = models.ForeignKey(
        ExternalCertificate, 
        on_delete=models.CASCADE, 
        verbose_name="校外证书"
    )
    obtain_date = models.DateField(verbose_name="获得时间")
    certificate_file = models.FileField(
        upload_to=certificate_upload_path,
        verbose_name="证书文件",
        help_text="支持图片(JPG, PNG)或PDF格式",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),],
        blank=True, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    notes = models.TextField(blank=True, verbose_name="备注")
    
    class Meta:
        verbose_name = "教师校外证书"
        verbose_name_plural = "教师校外证书"
        ordering = ['-obtain_date']
        
    def __str__(self):
        return f"{self.teacher} - {self.external_certificate} ({self.obtain_date.year})"
    
    def file_extension(self):
        name, extension = os.path.splitext(self.certificate_file.name)
        return extension.lower()
    
    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        return self.file_extension() in image_extensions
    
    def is_pdf(self):
        return self.file_extension() == '.pdf'
    
    
    
# 副班主任经历模型
class DeputyHeadTeacherExperience(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='deputy_head_teacher_experiences',
        verbose_name="教师"
    )
    school_year = models.CharField(max_length=200, verbose_name="学年")
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "副班主任经历"
        verbose_name_plural = "副班主任经历"
        ordering = ['-school_year']

    def __str__(self):
        return f"{self.teacher} - {self.school_year}"
    
    
    
# 年度考核模型
class AnnualAssessment(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='annual_assessments',
        verbose_name="教师"
    )
    year = models.CharField(max_length=200, verbose_name="年度")
    # 当年是否记功，默认是否
    merit = models.BooleanField(default=False, verbose_name="记功")
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    
    class Meta:
        verbose_name = "年度考核"
        verbose_name_plural = "年度考核"
        ordering = ['-year']

    def __str__(self):
        return f"{self.teacher} - {self.year}"