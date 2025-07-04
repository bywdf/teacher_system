from django.utils.http import urlencode
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
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

# 在视图函数开头定义模型到URL名称的映射
MODEL_TO_URL_MAP = {
    # 文化课教师
    'TeacherMidAssess': 'cultura_mid_list',
    'TeacherFinalAssess': 'cultura_end_list',
    'TeacherSemesterAssess': 'cultura_term_list',
    
    # 音乐教师
    'MusicTeacherMidAssess': 'music_mid_list',
    'MusicTeacherFinalAssess': 'music_end_list',
    'MusicTeacherSemesterAssess': 'music_term_list',
    
    # 美术教师
    'ArtTeacherMidAssess': 'art_mid_list',
    'ArtTeacherFinalAssess': 'art_end_list',
    'ArtTeacherSemesterAssess': 'art_term_list',
    
    # 体育教师
    'PeTeacherMidAssess': 'pe_mid_list',
    'PeTeacherFinalAssess': 'pe_end_list',
    'PeTeacherSemester': 'pe_term_list',
    
    # 信息技术教师
    'ItTeacherMidAssess': 'it_mid_list',
    'ItTeacherFinalAssess': 'it_end_list',
    'ItTeacherSemester': 'it_term_list',
    
    # 组长考核
    'GroupLeaderMidAssess': 'groupleader_mid_list',
    'GroupLeaderFinalAssess': 'groupleader_end_list',
    'GroupLeaderSemester': 'groupleader_term_list',
    
    # 班主任考核
    'HeadTeacherMidAssess': 'headteacher_mid_list',
    'HeadTeacherFinalAssess': 'headteacher_end_list',
    'HeadTeacherSemester': 'headteacher_term_list',
    
    # 其他考核
    'EduAdmin': 'eduadmin_list',
    'ALAdmin': 'aladmin_list',
    'DeputyHeadTeacher': 'deputy_list',
}

@login_required
def my_assessments(request):
    user = request.user
    assessments = []
    
    # 定义获取期中/期末成绩的通用函数
    def add_assessments(model_class, assess_type, mid_model=None, final_model=None):
        # 获取学期总评成绩
        semester_assessments = model_class.objects.filter(teacher=user)
        for assess in semester_assessments:
            # 获取对应的URL名称
            url_name = MODEL_TO_URL_MAP.get(model_class.__name__)
            
            assessments.append({
                'type': assess_type,
                'semester': assess.semester,
                'term_type': assess.term_type.name if assess.term_type else "-",
                'assess_depart': assess.assess_depart.name,
                'mid_score': assess.mid_score.total_score if assess.mid_score else "-",
                'final_score': assess.final_score.total_score if assess.final_score else "-",
                'total_score': assess.total_score,
                'rank': assess.rank,
                'id': assess.id,
                'model': model_class.__name__,
                'url_name': url_name,  # 添加URL名称
                'teacher_id': assess.teacher.id,
                'semester_id': assess.semester.id,
            })
        
        # 直接获取期中成绩（若存在独立记录）
        if mid_model:
            mid_assessments = mid_model.objects.filter(teacher=user)
            for assess in mid_assessments:
                url_name = MODEL_TO_URL_MAP.get(mid_model.__name__)
                
                assessments.append({
                    'type': f"{assess_type}（期中）",
                    'semester': assess.semester,
                    'term_type': assess.term_type.name if assess.term_type else "期中",
                    'assess_depart': assess.assess_depart.name,
                    'mid_score': assess.total_score,
                    'final_score': "-",
                    'total_score': assess.total_score,
                    'rank': assess.rank,
                    'id': assess.id,
                    'model': mid_model.__name__,
                    'url_name': url_name,  # 添加URL名称
                    'teacher_id': assess.teacher.id,
                    'semester_id': assess.semester.id,
                })
        
        # 直接获取期末成绩（若存在独立记录）
        if final_model:
            final_assessments = final_model.objects.filter(teacher=user)
            for assess in final_assessments:
                url_name = MODEL_TO_URL_MAP.get(final_model.__name__)
                
                assessments.append({
                    'type': f"{assess_type}（期末）",
                    'semester': assess.semester,
                    'term_type': assess.term_type.name if assess.term_type else "期末",
                    'assess_depart': assess.assess_depart.name,
                    'mid_score': "-",
                    'final_score': assess.total_score,
                    'total_score': assess.total_score,
                    'rank': assess.rank,
                    'id': assess.id,
                    'model': final_model.__name__,
                    'url_name': url_name,  # 添加URL名称
                    'teacher_id': assess.teacher.id,
                    'semester_id': assess.semester.id,
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
    
    # 教务员、行政后勤、副班主任考核
    edu_admin_assessments = EduAdmin.objects.filter(teacher=user)
    for assess in edu_admin_assessments:
        url_name = MODEL_TO_URL_MAP.get('EduAdmin')
        
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
            'model': 'EduAdmin',
            'url_name': url_name,  # 添加URL名称
            'teacher_id': assess.teacher.id,
            'semester_id': assess.semester.id,
        })
    
    al_admin_assessments = ALAdmin.objects.filter(teacher=user)
    for assess in al_admin_assessments:
        url_name = MODEL_TO_URL_MAP.get('ALAdmin')
        
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
            'model': 'ALAdmin',
            'url_name': url_name,  # 添加URL名称
            'teacher_id': assess.teacher.id,
            'semester_id': assess.semester.id,
        })
    
    deputy_assessments = DeputyHeadTeacher.objects.filter(teacher=user)
    for assess in deputy_assessments:
        url_name = MODEL_TO_URL_MAP.get('DeputyHeadTeacher')
        
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
            'model': 'DeputyHeadTeacher',
            'url_name': url_name,  # 添加URL名称
            'teacher_id': assess.teacher.id,
            'semester_id': assess.semester.id,
        })
    
    # 按学期排序
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
    
    # 分页处理
    grouped_list = list(grouped_assessments.values())
    paginator = Paginator(grouped_list, 9)  # 每页显示9个分组
    page = request.GET.get('page')
    
    try:
        paginated_groups = paginator.page(page)
    except PageNotAnInteger:
        paginated_groups = paginator.page(1)
    except EmptyPage:
        paginated_groups = paginator.page(paginator.num_pages)    
    
    context = {
        'paginated_groups': paginated_groups,
        'user': user,
        'title': '个人考核记录',
    }
    return render(request, 'my_assessments.html', context)


@login_required
def assessment_detail(request, model_name, pk):
    MODEL_MAP = {
        'TeacherSemesterAssess': TeacherSemesterAssess,
        'TeacherMidAssess': TeacherMidAssess,
        'TeacherFinalAssess': TeacherFinalAssess,
        'MusicTeacherSemesterAssess': MusicTeacherSemesterAssess,
        'MusicTeacherMidAssess': MusicTeacherMidAssess,
        'MusicTeacherFinalAssess': MusicTeacherFinalAssess,
        'ArtTeacherSemesterAssess': ArtTeacherSemesterAssess,
        'ArtTeacherMidAssess': ArtTeacherMidAssess,
        'ArtTeacherFinalAssess': ArtTeacherFinalAssess,
        'PeTeacherSemester': PeTeacherSemester,
        'PeTeacherMidAssess': PeTeacherMidAssess,
        'PeTeacherFinalAssess': PeTeacherFinalAssess,
        'ItTeacherSemester': ItTeacherSemester,
        'ItTeacherMidAssess': ItTeacherMidAssess,
        'ItTeacherFinalAssess': ItTeacherFinalAssess,
        'GroupLeaderSemester': GroupLeaderSemester,
        'GroupLeaderMidAssess': GroupLeaderMidAssess,
        'GroupLeaderFinalAssess': GroupLeaderFinalAssess,
        'HeadTeacherSemester': HeadTeacherSemester,
        'HeadTeacherMidAssess': HeadTeacherMidAssess,
        'HeadTeacherFinalAssess': HeadTeacherFinalAssess,
        'EduAdmin': EduAdmin,
        'ALAdmin': ALAdmin,
        'DeputyHeadTeacher': DeputyHeadTeacher
    }
    
    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        return render(request, '404.html', status=404)
    
    assessment = get_object_or_404(model_class, pk=pk, teacher=request.user)
    
    # 准备返回列表的URL
    back_to_list_url = None
    url_name = MODEL_TO_URL_MAP.get(model_name)
    if url_name:
        # 构建查询参数
        params = {
            'teacher_name': request.user.name,
            'semester': assessment.semester.id
        }
        # 使用urlencode确保参数正确编码
        query_string = urlencode(params)
        back_to_list_url = f"{reverse('assessments:' + url_name)}?{query_string}"
    
    context = {
        'assessment': assessment,
        'model_name': model_name,
        'is_readonly': True,
        'back_to_list_url': back_to_list_url,
    }
    return render(request, 'assessment_detail.html', context)