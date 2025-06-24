from django.urls import path
from assessments.views import cultura_mid, semester, assessdepart, cultura_end, cultura_term, music_mid, music_end, music_term, art_mid, art_end

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
    
    # 音乐教师期中考核管理
    path('music/midlist/', music_mid.music_mid_list, name='music_mid_list'),
    path('music/midadd/', music_mid.music_mid_add, name='music_mid_add'),
    path('music/middelete/', music_mid.music_mid_delete, name='music_mid_delete'),
    path('music/midedit/<int:pk>',music_mid.music_mid_edit, name='music_mid_edit'),
    path('music/midimport/', music_mid.music_mid_import, name='music_mid_import'),
    path('music/mid/export/', music_mid.music_mid_export, name='music_mid_export'),
    path('music_mid/update_rank/', music_mid.music_mid_update_rank, name='music_mid_update_rank'),
    # 音乐期末考核管理
    path('music/endlist/', music_end.music_end_list, name='music_end_list'),
    path('music/endadd/', music_end.music_end_add, name='music_end_add'),
    path('music/enddelete/', music_end.music_end_delete, name='music_end_delete'),
    path('music/endedit/<int:pk>', music_end.music_end_edit, name='music_end_edit'),
    path('music/endimport/', music_end.music_end_import, name='music_end_import'),
    path('music/end/export/', music_end.music_end_export, name='music_end_export'),
    path('music_end/update_rank/', music_end.music_end_update_rank, name='music_end_update_rank'),
    # 音乐学期管理url
    path('music/termlist/', music_term.music_term_list, name='music_term_list'),
    path('music/termadd/', music_term.music_term_add, name='music_term_add'),
    path('music/termdelete/', music_term.music_term_delete, name='music_term_delete'),
    path('music/termedit/<int:pk>', music_term.music_term_edit, name='music_term_edit'),
    path('music/termimport/', music_term.music_term_import, name='music_term_import'),
    path('music/term/export/', music_term.music_term_export, name='music_term_export'),
    path('music_term/update_rank/', music_term.music_term_update_rank, name='music_term_update_rank'),
    
    # 美术教师期中考核管理
    path('art/midlist/', art_mid.art_mid_list, name='art_mid_list'),
    path('art/midadd/', art_mid.art_mid_add, name='art_mid_add'),
    path('art/middelete/', art_mid.art_mid_delete, name='art_mid_delete'),
    path('art/midedit/<int:pk>', art_mid.art_mid_edit, name='art_mid_edit'),
    path('art/midimport/', art_mid.art_mid_import, name='art_mid_import'),
    path('art/mid/export/', art_mid.art_mid_export, name='art_mid_export'),
    path('art_mid/update_rank/', art_mid.art_mid_update_rank, name='art_mid_update_rank'),
    # 美术期末考核管理
    path('art/endlist/', art_end.art_end_list, name='art_end_list'),
    path('art/endadd/', art_end.art_end_add, name='art_end_add'),
    path('art/enddelete/', art_end.art_end_delete, name='art_end_delete'),
    path('art/endedit/<int:pk>', art_end.art_end_edit, name='art_end_edit'),
    path('art/endimport/', art_end.art_end_import, name='art_end_import'),
    path('art/end/export/', art_end.art_end_export, name='art_end_export'),
    path('art_end/update_rank/', art_end.art_end_update_rank, name='art_end_update_rank'),
]