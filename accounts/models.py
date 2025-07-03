from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os


# Create your models here.


class Department(models.Model):
    """年级（部门）"""
    title = models.CharField(max_length=100, verbose_name="年级（部门）")

    def __str__(self):
        return self.title


class Subject(models.Model):
    """任教学科"""
    title = models.CharField(max_length=100, verbose_name="学科")

    def __str__(self):
        return self.title


class UserInfo(AbstractUser):
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True, verbose_name="头像")
    name = models.CharField(max_length=100, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    # 参加工作时间
    work_time = models.CharField(verbose_name="参加工作时间", blank=True, null=True)
    # 入党时间
    party_time = models.CharField(verbose_name="入党时间", blank=True, null=True)
    idnumber = models.CharField(
        max_length=18, verbose_name="身份证号", blank=True, null=True)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(
        verbose_name='性别', choices=gender_choices, default=1)
    phone = models.CharField(max_length=11, verbose_name="电话")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, verbose_name="所属年级（部门）")
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, verbose_name="任教学科")
    
    
    # 民族
    nation = models.CharField(verbose_name="民族", max_length=100, blank=True, null=True)
    # 政治面貌
    political_status = models.CharField(verbose_name="政治面貌", max_length=100, blank=True, null=True)
    # 籍贯
    native_place = models.CharField(verbose_name="籍贯", max_length=100, blank=True, null=True)
    # 现住址
    address = models.CharField(verbose_name="现住址", max_length=100, blank=True, null=True)

    
    
    # 第一学历
    first_education = models.CharField(verbose_name="第一学历", max_length=100, blank=True, null=True)
    # 第一学历毕业院校
    first_education_school = models.CharField(verbose_name="第一学历毕业院校", max_length=100, blank=True, null=True)
    # 第一学历专业
    first_education_major = models.CharField(verbose_name="第一学历专业", max_length=100, blank=True, null=True)
    # 第一学历毕业时间
    first_education_time = models.DateField(verbose_name="第一学历毕业时间", blank=True, null=True)
    # 最高学历
    highest_education = models.CharField(verbose_name="最高学历", max_length=100, blank=True, null=True)
    # 最高学历毕业院校
    highest_education_school = models.CharField(verbose_name="最高学历毕业院校", max_length=100, blank=True, null=True)
    # 最高学历专业
    highest_education_major = models.CharField(verbose_name="最高学历专业", max_length=100, blank=True, null=True)
    # 最高学历毕业时间
    highest_education_time = models.DateField(verbose_name="最高学历毕业时间", blank=True, null=True)
    
    # 专业资格
    professional_qualification = models.CharField(verbose_name="专业资格", max_length=100, blank=True, null=True)
    professional_qualification_time = models.CharField(verbose_name="专业资格取得时间", blank=True, null=True)
    # 职称及聘任时间
    professional_title = models.CharField(verbose_name="聘任职称", max_length=100, blank=True, null=True)
    professional_title_time = models.CharField(verbose_name="聘任时间", blank=True, null=True)        
    # 分级竞聘后聘任等级及时间
    appointment_grade = models.CharField(verbose_name="分级竞聘后聘任等级", max_length=100, blank=True, null=True)
    appointment_grade_time = models.CharField(verbose_name="分级竞聘后聘任时间", blank=True, null=True)
    # 调入我校时间
    transfer_time = models.CharField(verbose_name="调入我校时间", blank=True, null=True)
    
    # 保存方法可以简化，使用更健壮的路径处理
    def save(self, *args, **kwargs):
        # 确保上传时目录存在
        if self.avatar:
            # 获取完整上传路径（不含文件名）
            upload_dir = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.avatar.name))
            os.makedirs(upload_dir, exist_ok=True)
        super().save(*args, **kwargs)