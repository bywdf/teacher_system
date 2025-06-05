from django.db import models
from django.contrib.auth.models import AbstractUser

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


class User(AbstractUser):
    username = models.CharField(
        max_length=100, unique=True, verbose_name="用户名")
    name = models.CharField(max_length=100, verbose_name="姓名")
    idnumber = models.CharField(
        max_length=18, unique=True, verbose_name="身份证号", blank=True, null=True)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(
        verbose_name='性别', choices=gender_choices, default=1)
    email = models.EmailField(
        verbose_name="邮箱", unique=True,  blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name="电话")
    password = models.CharField(max_length=100, verbose_name="密码")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, verbose_name="所属年级（部门）")
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, verbose_name="任教学科")
