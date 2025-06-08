from django.urls import path
from assessments.views import semester, assessdepart, culturassess

app_name = 'assessments'

urlpatterns = [
    # 学年管理
    path('semester/list/', semester.semester_list, name='semester_list'),
    path('semester/add/', semester.semester_add, name='semester_add'),
    path('semester/delete/', semester.semester_delete, name='semester_delete'),
    path('semester/detail/', semester.semester_detail, name='semester_detail'),
    path('semester/edit/', semester.semester_edit, name='semester_edit'),
    
    # 考核分组管理
    path('assessdepart/list/', assessdepart.assessdepart_list, name='assessdepart_list'),
    path('assessdepart/add/', assessdepart.assessdepart_add, name='assessdepart_add'),
    path('assessdepart/delete/', assessdepart.assessdepart_delete, name='assessdepart_delete'),
    path('assessdepart/detail/', assessdepart.assessdepart_detail, name='assessdepart_detail'),
    path('assessdepart/edit/', assessdepart.assessdepart_edit, name='assessdepart_edit'),
    path('assessdepart/import/', assessdepart.assessdepart_import, name='assessdepart_import'),
    
    # 文化课教师考核管理
    path('cultura/midlist/', culturassess.cultura_mid_list, name='cultura_mid_list'),
]