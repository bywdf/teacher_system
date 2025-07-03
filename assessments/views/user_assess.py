from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import UserInfo
from assessments.models import (
    # 基础模型
    Semester, TermType, AssessDepart,
    # 文化课教师考核
    TeacherMidAssess, TeacherFinalAssess, TeacherSemesterAssess,
    # 音乐教师考核
    MusicTeacherMidAssess, MusicTeacherFinalAssess, MusicTeacherSemesterAssess,
    # 美术教师考核
    ArtTeacherMidAssess, ArtTeacherFinalAssess, ArtTeacherSemesterAssess,
    # 体育教师考核
    PeTeacherMidAssess, PeTeacherFinalAssess, PeTeacherSemester,
    # 信息技术教师考核
    ItTeacherMidAssess, ItTeacherFinalAssess, ItTeacherSemester,
    # 组长考核
    GroupLeaderMidAssess, GroupLeaderFinalAssess, GroupLeaderSemester,
    # 班主任考核
    HeadTeacherMidAssess, HeadTeacherFinalAssess, HeadTeacherSemester,
    # 其他考核
    EduAdmin, ALAdmin, DeputyHeadTeacher
)

@login_required
def my_assessments(request):
    user = request.user
    assessments = []
    
    # 定义获取期中/期末成绩的通用函数
    def add_assessments(model_class, assess_type, mid_model=None, final_model=None):
        # 获取学期总评成绩
        semester_assessments = model_class.objects.filter(teacher=user)
        for assess in semester_assessments:
            # 从学期总评中获取期中/期末成绩
            mid_score = assess.mid_score.total_score if assess.mid_score else "-"
            final_score = assess.final_score.total_score if assess.final_score else "-"
            # 从关联对象获取term_type
            term_type_obj = assess.term_type
            term_type_name = term_type_obj.name if term_type_obj else "-"
            
            assessments.append({
                'type': assess_type,
                'semester': assess.semester,
                'term_type': term_type_name,
                'assess_depart': assess.assess_depart.name,
                'mid_score': mid_score,
                'final_score': final_score,
                'total_score': assess.total_score,
                'rank': assess.rank,
                'id': assess.id,
                'model': model_class.__name__
            })
        
        # 直接获取期中成绩（若存在独立记录）
        if mid_model:
            mid_assessments = mid_model.objects.filter(teacher=user)
            for assess in mid_assessments:
                term_type_name = assess.term_type.name if assess.term_type else "期中"
                assessments.append({
                    'type': f"{assess_type}（期中）",
                    'semester': assess.semester,
                    'term_type': term_type_name,
                    'assess_depart': assess.assess_depart.name,
                    'mid_score': assess.total_score,
                    'final_score': "-",
                    'total_score': assess.total_score,
                    'rank': assess.rank,
                    'id': assess.id,
                    'model': mid_model.__name__
                })
        
        # 直接获取期末成绩（若存在独立记录）
        if final_model:
            final_assessments = final_model.objects.filter(teacher=user)
            for assess in final_assessments:
                term_type_name = assess.term_type.name if assess.term_type else "期末"
                assessments.append({
                    'type': f"{assess_type}（期末）",
                    'semester': assess.semester,
                    'term_type': term_type_name,
                    'assess_depart': assess.assess_depart.name,
                    'mid_score': "-",
                    'final_score': assess.total_score,
                    'total_score': assess.total_score,
                    'rank': assess.rank,
                    'id': assess.id,
                    'model': final_model.__name__
                })
                
        if final_model:
            final_assessments = final_model.objects.filter(teacher=user)
            for assess in final_assessments:
                assessments.append({
                    'type': f"{assess_type}（期末）",
                    'semester': assess.semester,
                    'term_type': assess.term_type.name if assess.term_type else "-",
                    'assess_depart': assess.assess_depart.name,
                    'mid_score': "-",
                    'final_score': assess.total_score,
                    'total_score': assess.total_score,
                    'rank': assess.rank,
                    'id': assess.id,
                    'model': final_model.__name__
                })
    
    # 文化课教师考核
    add_assessments(
        TeacherSemesterAssess, "文化课教师", 
        mid_model=TeacherMidAssess, 
        final_model=TeacherFinalAssess
    )
    
    # 音乐教师考核
    add_assessments(
        MusicTeacherSemesterAssess, "音乐教师", 
        mid_model=MusicTeacherMidAssess, 
        final_model=MusicTeacherFinalAssess
    )
    
    # 美术教师考核
    add_assessments(
        ArtTeacherSemesterAssess, "美术教师", 
        mid_model=ArtTeacherMidAssess, 
        final_model=ArtTeacherFinalAssess
    )
    
    # 体育教师考核
    add_assessments(
        PeTeacherSemester, "体育教师", 
        mid_model=PeTeacherMidAssess, 
        final_model=PeTeacherFinalAssess
    )
    
    # 信息技术教师考核
    add_assessments(
        ItTeacherSemester, "信息技术教师", 
        mid_model=ItTeacherMidAssess, 
        final_model=ItTeacherFinalAssess
    )
    
    # 组长考核
    add_assessments(
        GroupLeaderSemester, "组长", 
        mid_model=GroupLeaderMidAssess, 
        final_model=GroupLeaderFinalAssess
    )
    
    # 班主任考核
    add_assessments(
        HeadTeacherSemester, "班主任", 
        mid_model=HeadTeacherMidAssess, 
        final_model=HeadTeacherFinalAssess
    )
    
    # 教务员、行政后勤、副班主任考核（无期中/期末区分，直接添加）
    edu_admin_assessments = EduAdmin.objects.filter(teacher=user)
    for assess in edu_admin_assessments:
        assessments.append({
            'type': '教务员',
            'semester': assess.semester,
            'term_type': assess.term_type.name if assess.term_type else "-",
            'assess_depart': assess.assess_depart.name,
            'mid_score': "-",
            'final_score': "-",
            'total_score': assess.total_score,
            'rank': assess.rank,
            'id': assess.id,
            'model': 'EduAdmin'
        })
    
    al_admin_assessments = ALAdmin.objects.filter(teacher=user)
    for assess in al_admin_assessments:
        assessments.append({
            'type': '行政后勤',
            'semester': assess.semester,
            'term_type': assess.term_type.name if assess.term_type else "-",
            'assess_depart': assess.assess_depart.name,
            'mid_score': "-",
            'final_score': "-",
            'total_score': assess.total_score,
            'rank': assess.rank,
            'id': assess.id,
            'model': 'ALAdmin'
        })
    
    deputy_assessments = DeputyHeadTeacher.objects.filter(teacher=user)
    for assess in deputy_assessments:
        assessments.append({
            'type': '副班主任',
            'semester': assess.semester,
            'term_type': assess.term_type.name if assess.term_type else "-",
            'assess_depart': assess.assess_depart.name,
            'mid_score': "-",
            'final_score': "-",
            'total_score': assess.total_score,
            'rank': assess.rank,
            'id': assess.id,
            'model': 'DeputyHeadTeacher'
        })
    
    # 按学期排序（先按年份降序，再按学期类型降序）
    assessments.sort(key=lambda x: (x['semester'].year, x['semester'].semester_type), reverse=True)
    
    # 按学期和考核部门分组
    grouped_assessments = {}
    for assess in assessments:
        key = f"{assess['semester']}-{assess['assess_depart']}"
        if key not in grouped_assessments:
            grouped_assessments[key] = {
                'semester': assess['semester'],
                'assess_depart': assess['assess_depart'],
                'assessments': []
            }
        grouped_assessments[key]['assessments'].append(assess)
    
    context = {
        'grouped_assessments': grouped_assessments.values(),
        'user': user,
        'title': '个人考核记录',
    }
    return render(request, 'my_assessments.html', context)

@login_required
def assessment_detail(request, model_name, pk):
    MODEL_MAP = {
        'TeacherSemesterAssess': TeacherSemesterAssess,
        'MusicTeacherSemesterAssess': MusicTeacherSemesterAssess,
        'ArtTeacherSemesterAssess': ArtTeacherSemesterAssess,
        'PeTeacherSemester': PeTeacherSemester,
        'ItTeacherSemester': ItTeacherSemester,
        'GroupLeaderSemester': GroupLeaderSemester,
        'HeadTeacherSemester': HeadTeacherSemester,
        'EduAdmin': EduAdmin,
        'ALAdmin': ALAdmin,
        'DeputyHeadTeacher': DeputyHeadTeacher
    }
    
    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return render(request, '404.html', status=404)
    
    assessment = get_object_or_404(model_class, pk=pk, teacher=request.user)
    
    context = {
        'assessment': assessment,
        'model_name': model_name
    }
    return render(request, 'assessment_detail.html', context)