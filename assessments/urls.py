from django.urls import path
from assessments.views import cultura_mid, semester, assessdepart

app_name = 'assessments'

urlpatterns = [
    # 学年管理
    path('semester/list/', semester.semester_list, name='semester_list'),
    path('semester/add/', semester.semester_add, name='semester_add'),
    path('semester/delete/', semester.semester_delete, name='semester_delete'),
    path('semester/detail/', semester.semester_detail, name='semester_detail'),
    path('semester/edit/', semester.semester_edit, name='semester_edit'),
    
    # 考核部门管理
    path('assessdepart/list/', assessdepart.assessdepart_list, name='assessdepart_list'),
    path('assessdepart/add/', assessdepart.assessdepart_add, name='assessdepart_add'),
    path('assessdepart/delete/', assessdepart.assessdepart_delete, name='assessdepart_delete'),
    path('assessdepart/detail/', assessdepart.assessdepart_detail, name='assessdepart_detail'),
    path('assessdepart/edit/', assessdepart.assessdepart_edit, name='assessdepart_edit'),
    path('assessdepart/import/', assessdepart.assessdepart_import, name='assessdepart_import'),
    
    # 文化课教师期中考核管理
    path('teacher_autocomplete/', cultura_mid.teacher_autocomplete, name='teacher_autocomplete'),
    path('cultura/midlist/', cultura_mid.cultura_mid_list, name='cultura_mid_list'),
    path('cultura/midadd/', cultura_mid.cultura_mid_add, name='cultura_mid_add'),
    path('cultura/middelete/', cultura_mid.cultura_mid_delete, name='cultura_mid_delete'),
    path('cultura/midedit/<int:pk>', cultura_mid.cultura_mid_edit, name='cultura_mid_edit'),
    path('cultura/midimport/', cultura_mid.cultura_mid_import, name='cultura_mid_import'),
    path('cultura/mid/export/', cultura_mid.cultura_mid_export, name='cultura_mid_export'),

    
    
]