from django.db import models

from accounts.models import User

# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name()


class AssessDepart(models.Model):
    '''参与考核的部门'''
    pass


class TermYear(models.Model):
    """学年表"""
    name = models.CharField('学年名称', max_length=50, unique=True)
    # start_date = models.DateField('开始日期')
    # end_date = models.DateField('结束日期')
    # is_current = models.BooleanField('是否当前学期', default=False)
    # create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学年'
        verbose_name_plural = '学年'


class Semester(models.Model):
    '''学期表'''
    Semester_Choices = (
        ('last', '上学期'),
        ('next', '下学期'),
    )
    semester_type = models.CharField(max_length=20, choices=Semester_Choices)

    def __str__(self):
        return self.get_term_type_display()


class Term(models.Model):
    '''学期考核分类表'''
    Term_Choices = (
        ('mid', '期中考试'),
        ('final', '期末考试'),
        ('semester', '学期总评'),
    )
    term_type = models.CharField(max_length=20, choices=Term_Choices)

    def __str__(self):
        return self.get_term_type_display()
