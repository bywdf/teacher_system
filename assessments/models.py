from django.db import models
from django.forms import ValidationError

from accounts.models import UserInfo

# Create your models here.


class AssessDepart(models.Model):
    '''参与考核的部门类型'''
    name = models.CharField(verbose_name='参与考核部门', max_length=50, unique=True)
    
    class Meta:
        verbose_name = '参与考核部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class ALDepart(models.Model):
#     name = models.CharField(verbose_name='部门', max_length=50, unique=True)

#     class Meta:
#         verbose_name = '后勤部门'
#         verbose_name_plural = verbose_name
#     def __str__(self):
#         return self.name

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
        verbose_name = '学期'
        verbose_name_plural = verbose_name
        unique_together = ('year', 'semester_type')

    def __str__(self):
        return f"{self.year}{self.get_semester_type_display()}"


class TermType(models.Model):
    '''学期考核分类表'''
    name = models.CharField(max_length=50, verbose_name='学期考核类型', unique=True)
    
    class Meta:
        verbose_name = '考核类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TeacherBase(models.Model):
    '''文化课教师教师考核表(公共部分)'''
    week = models.IntegerField(verbose_name='考核周数')  # 考核周期(周数)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
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


class TeacherMidAssess(TeacherBase):
    '''文化课教师期中考核成绩'''
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')  # 添加唯一约束
        verbose_name = '文化课教师期中考核成绩'
        verbose_name_plural = '文化课教师期中考核成绩'
        
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
              
        # 工作量计算（带边界保护和总工作量为0的处理）
        if self.total_workload == 0:
            self.workload_score = 0.0
        else:
            weekly_workload = self.total_workload / self.week
        # 计算工作量成绩 并保留到3位小数
            self.workload_score = round(max(
                0, min(10, 4.5 + (weekly_workload - 10) * 0.1)), 3)

        # 总分计算
        scores = [
            self.workload_score,
            self.personal_score or 0,
            self.class_score or 0,
            self.group_score or 0
        ]
        self.total_score = round(sum(scores), 3)

        super().save(*args, **kwargs) 
    
    def __str__(self):
        # 返回格式："期中成绩(教师姓名, 学期): 总分"
        return f"期中成绩({self.teacher.name}, {self.semester}): {self.total_score or 0}"


class TeacherFinalAssess(TeacherBase):
    '''文化课教师期末考核成绩'''
    attend_score = models.FloatField(
        verbose_name='出勤成绩', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')  # 添加唯一约束
        verbose_name = '文化课教师期末考核成绩'
        verbose_name_plural = '文化课教师期末考核成绩'
        
    def __str__(self):
        # 返回格式："期末成绩(教师姓名, 学期): 总分"
        return f"期末成绩({self.teacher.name}, {self.semester}): {self.total_score or 0}"    

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
              
        # 工作量计算（带边界保护和总工作量为0的处理）
        if self.total_workload == 0:
            self.workload_score = 0.0
        else:
            weekly_workload = self.total_workload / self.week
            # 计算工作量成绩 并保留到3位小数
            self.workload_score = round(max(
                0, min(10, 4.5 + (weekly_workload - 10) * 0.1)), 3)
            
        # 总分计算
        scores = [
            self.workload_score,
            self.personal_score or 0,
            self.class_score or 0,
            self.group_score or 0,
            self.attend_score or 0,
            self.invigilation_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class TeacherSemesterAssess(models.Model):
    '''文化课教师学期总评成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    mid_score = models.ForeignKey(TeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(TeacherFinalAssess, on_delete=models.SET_NULL,
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
        self.total_score =round(mid + final, 3)
        super().save(*args, **kwargs)


class ArtTeacherBase(models.Model):
    '''艺术教师考核基础表'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    class_hours = models.FloatField(
        verbose_name='课堂教学节数', blank=True, null=True)
    major_hours = models.FloatField(
        verbose_name='专业课培训节数折算', blank=True, null=True)
    # 艺体活动与竞赛培训节数折算
    activity_hours = models.FloatField(verbose_name='艺体活动与竞赛培训节数折算', blank=True, null=True)
    extra_work_hours = models.FloatField(
        verbose_name='额外工作量', blank=True, null=True)
    total_workload = models.FloatField(
        verbose_name='总工作量节数', blank=True, null=True)
    workload_score = models.FloatField(
        verbose_name='课时工作量成绩', blank=True, null=True)
    teach_book = models.FloatField(
        verbose_name='常规教学薄成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        abstract = True
        verbose_name = '音乐美术教师考核底版'
        verbose_name_plural = '音乐美术教师考核底版'   


class MusicTeacherMidAssess(ArtTeacherBase):
    '''音乐教师期中考核成绩'''
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '音乐教师期中考核成绩'
        verbose_name_plural = '音乐教师期中考核成绩'
    
    def save(self, *args, **kwargs):
        
        scores = [
            self.workload_score or 0,
            self.teach_book or 0
        ]
        self.total_score = round(sum(scores), 3)

        super().save(*args, **kwargs)


class MusicTeacherFinalAssess(ArtTeacherBase):
    attend_score = models.FloatField(
        verbose_name='出勤成绩', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)
    # 艺考赋分
    art_score = models.FloatField(verbose_name='下学期艺考赋分', blank=True, null=True, default=0)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '音乐教师期末考核成绩'
        verbose_name_plural = '音乐教师期末考核成绩'

    def save(self, *args, **kwargs):
        
        # 防御性编程处理空值
        scores = [
            self.attend_score or 0,
            self.workload_score or 0,
            self.invigilation_score or 0,
            self.art_score or 0,
            self.teach_book or 0
        ]
        # 计算总成绩
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class MusicTeacherSemesterAssess(models.Model):
    '''音乐教师学期总评成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    mid_score = models.ForeignKey(MusicTeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(MusicTeacherFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(
        verbose_name='学期总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='学期名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '音乐教师学期总评成绩'
        verbose_name_plural = '音乐教师学期总评成绩'

    def save(self, *args, **kwargs):
        # 使用防御性编程处理空值
        mid = self.mid_score.total_score if self.mid_score else 0
        final = self.final_score.total_score if self.final_score else 0

        # 总成绩是期中期末直接相加,保留三位小数
        self.total_score =round(mid + final, 3)
        super().save(*args, **kwargs)


class ArtTeacherMidAssess(ArtTeacherBase):
    '''美术教师期中考核成绩'''
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '美术教师期中考核成绩'
        verbose_name_plural = '美术教师期中考核成绩'
        
    def save(self, *args, **kwargs):
        # 防御性处理空值
        scores = [
            self.workload_score or 0,
            self.teach_book or 0
        ]
        self.total_score = round(sum(scores), 3)
        # 保存
        super().save(*args, **kwargs)


class ArtTeacherFinalAssess(ArtTeacherBase):
    attend_score = models.FloatField(
        verbose_name='出勤成绩', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)
    # 艺考赋分
    art_score = models.FloatField(verbose_name='下学期艺考赋分', blank=True, null=True, default=0)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '美术教师期末考核成绩'
        verbose_name_plural = '美术教师期末考核成绩'

    def save(self, *args, **kwargs):
        
        # 防御性编程处理空值
        scores = [
            self.attend_score or 0,
            self.workload_score or 0,
            self.invigilation_score or 0,
            self.art_score or 0,
            self.teach_book or 0
        ]
        # 计算总成绩
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class ArtTeacherSemesterAssess(models.Model):
    '''美术教师学期总评成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    mid_score = models.ForeignKey(ArtTeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(ArtTeacherFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(
        verbose_name='学期总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='学期名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '美术教师学期总评成绩'
        verbose_name_plural = '美术教师学期总评成绩'

    def save(self, *args, **kwargs):
        # 使用防御性编程处理空值
        mid = self.mid_score.total_score if self.mid_score else 0
        final = self.final_score.total_score if self.final_score else 0

        # 总成绩是期中期末直接相加,保留三位小数
        self.total_score =round(mid + final, 3)
        super().save(*args, **kwargs)


class PeTeacherBase(models.Model):
    '''体育教师考核基础表'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    class_hours = models.FloatField(
        verbose_name='课堂教学节数', blank=True, null=True)
    major_hours = models.FloatField(
        verbose_name='专业课培训节数', blank=True, null=True)
    kejiancao_hours = models.FloatField(
        verbose_name='课间操、非工作日学校安排', blank=True, null=True)
    extra_work_hours = models.FloatField(
        verbose_name='额外工作量', blank=True, null=True)
    total_workload = models.FloatField(
        verbose_name='总工作量节数', blank=True, null=True)
    workload_score = models.FloatField(verbose_name='工作量成绩', blank=True, null=True)
    teach_book = models.FloatField(
        verbose_name='常规教学薄成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        abstract = True
        verbose_name = '体育教师考核底版'
        verbose_name_plural = '体育教师考核底版'


class PeTeacherMidAssess(PeTeacherBase):
    '''体育教师期中考核成绩'''
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '体育教师期中考核成绩'
        verbose_name_plural = '体育教师期中考核成绩'
        
    def save(self, *args, **kwargs):
        scores = [
            self.workload_score or 0,
            self.teach_book or 0,            
        ]
        # 计算总成绩
        self.total_score = round(sum(scores), 3)

        super().save(*args, **kwargs)



class PeTeacherFinalAssess(PeTeacherBase):
    '''体育教师期末考核成绩'''
    attend_score = models.FloatField(
        verbose_name='出勤成绩', blank=True, null=True)
    student_awards = models.FloatField(
        verbose_name='学生获奖得分', blank=True, null=True)
    ncee_awards = models.FloatField(
        verbose_name='高考成绩得分', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '体育教师期末考核成绩'
        verbose_name_plural = '体育教师期末考核成绩'

    def save(self, *args, **kwargs):
        # 确保覆盖任何手动输入的总成绩
        self.calculate_total_score()
        super().save(*args, **kwargs)
    
    def calculate_total_score(self):
        scores = [
            self.attend_score or 0,
            self.workload_score or 0,
            self.student_awards or 0,
            self.ncee_awards or 0,
            self.invigilation_score or 0,
            self.teach_book or 0
        ]
        self.total_score = round(sum(scores), 3)

class PeTeacherSemester(models.Model):
    '''体育教师学期总评成绩'''
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    mid_score = models.ForeignKey(PeTeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(PeTeacherFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '体育教师学期总评成绩'
        verbose_name_plural = '体育教师学期总评成绩'

    def save(self, *args, **kwargs):
        mid = self.mid_score.total_score or 0
        final = self.final_score.total_score or 0
        # 总成绩是期中成绩、期末成绩相加
        self.total_score = round(mid + final, 3)
        super().save(*args, **kwargs)


class ItTeacherbase(models.Model):
    '''信息技术教师考核底版'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    class_hours = models.FloatField(
        verbose_name='课堂教学节数', blank=True, null=True)
    video_hours = models.FloatField(
        verbose_name='录像、扫描等、校报等课时', blank=True, null=True)
    network_hours = models.FloatField(
        verbose_name='网络、维修等课时', blank=True, null=True)
    extra_work_hours = models.FloatField(
        verbose_name='额外工作量、托管', blank=True, null=True)
    total_workload = models.FloatField(
        verbose_name='总工作量节数', blank=True, null=True)
    workload_score = models.FloatField(verbose_name='工作量成绩', blank=True, null=True)
    teach_book = models.FloatField(
        verbose_name='常规教学薄成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        abstract = True
        

class ItTeacherMidAssess(ItTeacherbase):
    '''信息技术教师期中考核成绩'''
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '信息技术教师期中考核成绩'
        verbose_name_plural = '信息技术教师期中考核成绩'
    def save(self, *args, **kwargs):
        
        scores = [
            self.workload_score or 0,
            self.teach_book or 0,            
        ]        
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)



class ItTeacherFinalAssess(ItTeacherbase):
    '''信息技术教师期末考核成绩'''
    attend_score = models.FloatField(
        verbose_name='考勤得分', blank=True, null=True)
    invigilation_score = models.FloatField(
        verbose_name='监考成绩', blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '信息技术教师期末考核成绩'
        verbose_name_plural = '信息技术教师期末考核成绩'

    def save(self, *args, **kwargs):
        scores = [
            self.attend_score or 0,
            self.invigilation_score or 0,
            self.workload_score or 0,
            self.teach_book or 0,
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class ItTeacherSemester(models.Model):
    '''信息技术教师学期总评成绩'''
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    mid_score = models.ForeignKey(ItTeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(ItTeacherFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '信息技术教师学期总评成绩'
        verbose_name_plural = '信息技术教师学期总评成绩'

    def save(self, *args, **kwargs):       # 计算总成绩
        mid = self.mid_score.total_score or 0
        final = self.final_score.total_score or 0
        # 总成绩是期中成绩、期末成绩相加
        self.total_score = round(mid + final, 3)

        super().save(*args, **kwargs)


class GroupLeaderBase(models.Model):
    """组长考核成绩"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    plan_summary_score = models.FloatField(
        verbose_name='计划或总结得分', blank=True, null=True)
    teach_level_score = models.FloatField(
        verbose_name='教学水平(教学常规薄本评价)得分', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        scores = [
            self.plan_summary_score or 0,
            self.teach_level_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class GroupLeaderMidAssess(GroupLeaderBase):
    """组长期中考核成绩"""
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '组长期中考核成绩'
        verbose_name_plural = '组长期中考核成绩'


class GroupLeaderFinalAssess(GroupLeaderBase):
    """组长期末考核成绩"""
    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '组长期末考核成绩'
        verbose_name_plural = '组长期末考核成绩'


class GroupLeaderSemester(models.Model):
    """组长学期总评成绩"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    mid_score = models.ForeignKey(GroupLeaderMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(GroupLeaderFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester', 'term_type')
        verbose_name = '组长学期总评成绩'
        verbose_name_plural = '组长学期总评成绩'

    def save(self, *args, **kwargs):       # 计算总成绩
        mid = self.mid_score.total_score or 0
        final = self.final_score.total_score or 0
        # 总成绩是期中成绩、期末成绩相加
        self.total_score = round(mid + final, 3)

        super().save(*args, **kwargs)


class HeadTeacherBase(models.Model):
    """班主任考核底板"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    class_number = models.IntegerField(verbose_name='班级')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    manage_score = models.FloatField(
        verbose_name='常规管理考核成绩', blank=True, null=True)
    safety_score = models.FloatField(
        verbose_name='闭环式安全管理考核成绩', blank=True, null=True)
    class_score = models.FloatField(
        verbose_name='班级教学考核成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        scores = [
            self.manage_score or 0,
            self.safety_score or 0,
            self.class_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class HeadTeacherMidAssess(HeadTeacherBase):
    """班主任中期考核成绩"""
    class Meta:
        unique_together = ('semester', 'term_type', 'assess_depart','class_number')
        verbose_name = '班主任中期考核成绩'
        verbose_name_plural = '班主任中期考核成绩'


class HeadTeacherFinalAssess(HeadTeacherBase):
    """班主任期末考核成绩"""
    class Meta:
        unique_together = ('semester', 'term_type', 'assess_depart','class_number')
        verbose_name = '班主任期末考核成绩'
        verbose_name_plural = '班主任期末考核成绩'


class HeadTeacherSemester(models.Model):
    """班主任学期总评成绩"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='学期考核类型')
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    class_number = models.IntegerField(verbose_name='班级')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    mid_score = models.ForeignKey(HeadTeacherMidAssess, on_delete=models.SET_NULL,
                                  verbose_name='期中成绩', blank=True, null=True, related_name='mid_score')
    final_score = models.ForeignKey(HeadTeacherFinalAssess, on_delete=models.SET_NULL,
                                    verbose_name='期末成绩', blank=True, null=True, related_name='final_score')
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('semester', 'term_type', 'class_number')
        verbose_name = '班主任学期总评成绩'
        verbose_name_plural = '班主任学期总评成绩'

    def save(self, *args, **kwargs):       # 计算总成绩
        mid = self.mid_score.total_score or 0
        final = self.final_score.total_score or 0
        # 总成绩是期中成绩、期末成绩相加
        self.total_score = round(mid + final, 3)
        super().save(*args, **kwargs)


class EduAdmin(models.Model):
    """教务员考核表"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='考核类型', blank=True, null=True
    )
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    grade_depart = models.CharField(verbose_name="年级部", max_length=100, blank=True, null=True)
    # 考勤得分
    attend_score = models.FloatField(
        verbose_name='考勤得分', blank=True, null=True)
    # 出勤工作量折算
    attend_workload = models.FloatField(
        verbose_name='出勤工作量折算', blank=True, null=True)
    # 民主评议得分
    democratic_score = models.FloatField(
        verbose_name='民主评议得分', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester')
        verbose_name = '教务员考核表'
        verbose_name_plural = '教务员考核表'

    def save(self, *args, **kwargs):
        scores = [
            self.attend_score or 0,
            self.attend_workload or 0,
            self.democratic_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)
        
        
class ALAdmin(models.Model):
    """行政后勤考核表"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='考核类型', blank=True, null=True
    )
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    al_depart = models.CharField(verbose_name="后勤科室", max_length=100, blank=True, null=True)    
    # 考勤得分
    attend_score = models.FloatField(
        verbose_name='考勤得分', blank=True, null=True)
    # 出勤工作量折算
    attend_workload = models.FloatField(
        verbose_name='出勤工作量折算', blank=True, null=True)
    # 民主评议得分
    democratic_score = models.FloatField(
        verbose_name='民主评议得分', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester')
        verbose_name = '行政后勤考核表'
        verbose_name_plural = '行政后勤考核表'

    def save(self, *args, **kwargs):
        scores = [
            self.attend_score or 0,
            self.attend_workload or 0,
            self.democratic_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)


class DeputyHeadTeacher(models.Model):
    """副班主任考核表"""
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, verbose_name='学期')
    term_type = models.ForeignKey(
        TermType, on_delete=models.CASCADE, verbose_name='考核类型', blank=True, null=True
    )
    teacher = models.ForeignKey(
        UserInfo, on_delete=models.CASCADE, verbose_name='教师')
    assess_depart = models.ForeignKey(
        AssessDepart, on_delete=models.CASCADE, verbose_name='此次参与考核部门')
    assess_time = models.CharField(
        max_length=50, verbose_name='考核时间', blank=True, null=True)
    class_number = models.IntegerField(
        verbose_name='班级', blank=True, null=True)
    # 问卷评价得分
    questionnaire_score = models.FloatField(
        verbose_name='问卷评价得分', blank=True, null=True)
    # 工作过程评价
    work_process_score = models.FloatField(
        verbose_name='工作过程评价', blank=True, null=True)
    # 工作心得
    work_experience_score = models.FloatField(
        verbose_name='工作心得', blank=True, null=True)
    # 民主评议得分
    democratic_score = models.FloatField(
        verbose_name='民主评议得分', blank=True, null=True)
    # 班级边缘生帮扶评价
    edge_student_score = models.FloatField(
        verbose_name='班级边缘生帮扶评价', blank=True, null=True)
    class_score = models.FloatField(
        verbose_name='班级综合管理考核成绩', blank=True, null=True)
    total_score = models.FloatField(verbose_name='总成绩', blank=True, null=True)
    rank = models.FloatField(verbose_name='名次', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    is_published = models.BooleanField(verbose_name="是否公布", default=False)

    class Meta:
        unique_together = ('teacher', 'semester')
        verbose_name = '副班主任考核表'
        verbose_name_plural = '副班主任考核表'

    def save(self, *args, **kwargs):
        scores = [
            self.questionnaire_score or 0,
            self.work_process_score or 0,
            self.work_experience_score or 0,
            self.democratic_score or 0,
            self.edge_student_score or 0,
            self.class_score or 0
        ]
        self.total_score = round(sum(scores), 3)
        super().save(*args, **kwargs)
