from django.urls import path
from assessments.views import cultura_mid, semester, assessdepart, cultura_end, cultura_term, music_mid

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
    path('cultura_mid/update_rank/', cultura_mid.cultura_mid_update_rank, name='cultura_mid_update_rank'),
    # 文化科期末考核管理
    path('cultura/endllist/', cultura_end.cultura_end_list, name='cultura_end_list'),
    path('cultura/endadd/', cultura_end.cultura_end_add, name='cultura_end_add'),
    path('cultura/enddelete/', cultura_end.cultura_end_delete, name='cultura_end_delete'),
    path('cultura/endedit/<int:pk>', cultura_end.cultura_end_edit, name='cultura_end_edit'),
    path('cultura/endimport/', cultura_end.cultura_end_import, name='cultura_end_import'),
    path('cultura_end/update_rank/', cultura_end.cultura_end_update_rank, name='cultura_end_update_rank'),
    path('cultura/end/export/', cultura_end.cultura_end_export, name='cultura_end_export'),   
    # 文化科教师学期考核管理
    path('cultura/termlist/', cultura_term.cultura_term_list, name='cultura_term_list'),
    path('cultura/termadd/', cultura_term.cultura_term_add, name='cultura_term_add'),
    path('cultura/termdelete/', cultura_term.cultura_term_delete, name='cultura_term_delete'),
    path('cultura/termedit/<int:pk>', cultura_term.cultura_term_edit, name='cultura_term_edit'),
    path('cultura/termimport/', cultura_term.cultura_term_import, name='cultura_term_import'),
    path('cultura_term/update_rank/', cultura_term.cultura_term_update_rank, name='cultura_term_update_rank'),
    path('cultura/term/export/', cultura_term.cultura_term_export, name='cultura_term_export'),
    
    #音乐教师期中考核管理
    path('music/midlist/', music_mid.music_mid_list, name='music_mid_list'),
    path('music/midadd/', music_mid.music_mid_add, name='music_mid_add'),
    path('music/middelete/', music_mid.music_mid_delete, name='music_mid_delete'),
    path('music/midedit/<int:pk>',music_mid.music_mid_edit, name='music_mid_edit'),
    path('music/midimport/', music_mid.music_mid_import, name='music_mid_import'),
    path('music/mid/export/', music_mid.music_mid_export, name='music_mid_export'),
    path('music_mid/update_rank/', music_mid.music_mid_update_rank, name='music_mid_update_rank'),
]