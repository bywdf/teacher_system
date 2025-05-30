from django.db import models
from django.forms import ValidationError

from accounts.models import User

# Create your models here.


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='teacher_profile')

    def __str__(self):
        return self.user.name()


class AssessDepart(models.Model):
    '''参与考核的部门类型'''
    name = models.CharField(verbose_name='参与考核部门', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Semester(models.Model):
    '''学期表'''
    year = models.CharField(max_length=20, verbose_name='学年')
    Semester_Choices = (
        ('last', '上学期'),
        ('next', '下学期'),
    )
    semester_type = models.CharField(
        max_length=20, choices=Semester_Choices, verbose_name='学期')

    class Meta:
        unique_together = ('year', 'semester_type')

    def __str__(self):
        return f"{self.year}{self.get_semester_type_display()}"


class TermType(models.Model):
    '''学期考核分类表'''
    Term_Choices = (
        ('mid', '期中考试'),
        ('final', '期末考试'),
        ('semester', '学期总评'),
    )
    term_type = models.CharField(max_length=20, choices=Term_Choices)
    start_date = models.DateField()  # 考核开始日期
    end_date = models.DateField()   # 考核结束日期

    def __str__(self):
        return self.get_term_type_display()


class TeacherBase(models.Model):
    '''文化课教师教师考核表(公共部分)'''
    week = models.IntegerField()  # 考核周期(周数)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    class_hours = models.IntegerField(
        verbose_name='课时节数', blank=True, null=True, default=0)
    duty_hours = models.FloatField(
        verbose_name='值班节数折算', blank=True, null=True, default=0)
    extra_work_hours = models.FloatField(
        verbose_name='额外工作节数折算', blank=True, null=True, default=0)
    total_workload = models.FloatField(
        verbose_name='总工作量节数', blank=True, null=True)
    workload_score = models.FloatField(
        verbose_name='课时工作量成绩', blank=True, null=True)
    personal_score = models.FloatField(
        verbose_name='教师个人成绩', blank=True, null=True, default=0)
    class_score = models.FloatField(
        verbose_name='班级量化成绩', blank=True, null=True, default=0)
    group_score = models.FloatField(
        verbose_name='教研组量化成绩', blank=True, null=True, default=0)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # 验证周数
        if not hasattr(self, 'week') or self.week <= 0:
            raise ValidationError("考核周数必须为正整数")

        # 空值安全处理
        workloads = [
            self.class_hours or 0,
            self.duty_hours or 0,
            self.extra_work_hours or 0
        ]
        self.total_workload = sum(workloads)

        # 工作量计算（带边界保护）
        weekly_workload = self.total_workload / self.week
        self.workload_score = max(
            0, min(10, 4.5 + (weekly_workload - 10) * 0.1))

        # 总分计算
        scores = [
            self.workload_score,
            self.personal_score or 0,
            self.class_score or 0,
            self.group_score or 0
        ]
        self.total_score = round(sum(scores), 3)

        super().save(*args, **kwargs)


class TeacherMidAccess(TeacherBase):
    '''文化课教师期中考核成绩'''
    class Meta:
        verbose_name = '文化课教师期中考核成绩'
        verbose_name_plural = '文化课教师期中考核成绩'


class TeacherFinalAccess(TeacherBase):
    '''文化课教师期末考核成绩'''
    attend_score = models.FloatField(
        verbose_name='出勤成绩', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)

    class Meta:
        verbose_name = '文化课教师期末考核成绩'
        verbose_name_plural = '文化课教师期末考核成绩'

    def save(self, *args, **kwargs):
        # 计算总成绩时包含考勤和监考得分
        self.total_score = (
            self.attend_score +
            self.workload_score +
            self.personal_score +
            self.class_score +
            self.group_score +
            self.invigilation_score
        )
        super().save(*args, **kwargs)


class TeacherSemesterAccess(models.Model):
    '''文化课教师学期总评成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    mid_score = models.ForeignKey(TeacherMidAccess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(TeacherFinalAccess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(
        verbose_name='学期总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='学期名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'semester')  # 添加唯一约束
        verbose_name = '文化课教师学期总评成绩'
        verbose_name_plural = '文化课教师学期总评成绩'

    def save(self, *args, **kwargs):
        # 使用防御性编程处理空值
        mid = self.mid_score.total_score if self.mid_score else 0
        final = self.final_score.total_score if self.final_score else 0

        # 总成绩是期中期末直接相加,保留三位小数
        self.total_score = mid + final
        super().save(*args, **kwargs)


class ArtTeacherBase(models.Model):
    '''艺术教师考核成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    class_hours = models.FloatField(verbose_name='课堂教学节数', blank=True, null=True)
    major_hours = models.FloatField(verbose_name='专业课培训节数', blank=True, null=True)
    extra_work_hours = models.FloatField(verbose_name='额外工作量', blank=True, null=True)
    total_workload = models.FloatField(
        verbose_name='总工作量节数', blank=True, null=True)
    workload_score = models.FloatField(
        verbose_name='课时工作量成绩', blank=True, null=True)
    teach_book = models.FloatField(verbose_name='常规教学薄成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    class Meta:
        abstract = True
        verbose_name = '艺术教师考核成绩'
        verbose_name_plural = '艺术教师考核成绩'
     