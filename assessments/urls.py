from django.urls import path
from assessments.views import semester, assessdepart
from assessments.views import cultura_mid, cultura_end, cultura_term
from assessments.views import music_mid, music_end, music_term, art_mid, art_end, art_term
from assessments.views import pe_mid, pe_end, pe_term
from assessments.views import it_mid, it_end, it_term
from assessments.views import groupleader_mid, groupleader_end, groupleader_term
from assessments.views import headteacher_mid, headteacher_end, headteacher_term
from assessments.views import eduadmin, aladmin, deputy

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
    # 美术学期管理url
    path('art/termlist/', art_term.art_term_list, name='art_term_list'),
    path('art/termadd/', art_term.art_term_add, name='art_term_add'),
    path('art/termdelete/', art_term.art_term_delete, name='art_term_delete'),
    path('art/termedit/<int:pk>', art_term.art_term_edit, name='art_term_edit'),
    path('art/termimport/', art_term.art_term_import, name='art_term_import'),
    path('art/term/export/', art_term.art_term_export, name='art_term_export'),
    path('art_term/update_rank/', art_term.art_term_update_rank, name='art_term_update_rank'),
    
    # 体育教师期中考核管理
    path('pe/midlist/', pe_mid.pe_mid_list, name='pe_mid_list'),
    path('pe/midadd/', pe_mid.pe_mid_add, name='pe_mid_add'),
    path('pe/middelete/', pe_mid.pe_mid_delete, name='pe_mid_delete'),
    path('pe/midedit/<int:pk>', pe_mid.pe_mid_edit, name='pe_mid_edit'),
    path('pe/midimport/', pe_mid.pe_mid_import, name='pe_mid_import'),
    path('pe/mid/export/', pe_mid.pe_mid_export, name='pe_mid_export'),
    path('pe_mid/update_rank/', pe_mid.pe_mid_update_rank, name='pe_mid_update_rank'),
    # 体育期末考核管理
    path('pe/endlist/', pe_end.pe_end_list, name='pe_end_list'),
    path('pe/endadd/', pe_end.pe_end_add, name='pe_end_add'),
    path('pe/enddelete/', pe_end.pe_end_delete, name='pe_end_delete'),
    path('pe/endedit/<int:pk>', pe_end.pe_end_edit, name='pe_end_edit'),
    path('pe/endimport/', pe_end.pe_end_import, name='pe_end_import'),
    path('pe/end/export/', pe_end.pe_end_export, name='pe_end_export'),
    path('pe_end/update_rank/', pe_end.pe_end_update_rank, name='pe_end_update_rank'),
    # 体育学期管理
    path('pe/termlist/', pe_term.pe_term_list, name='pe_term_list'),
    path('pe/termadd/', pe_term.pe_term_add, name='pe_term_add'),
    path('pe/termdelete/', pe_term.pe_term_delete, name='pe_term_delete'),
    path('pe/termedit/<int:pk>', pe_term.pe_term_edit, name='pe_term_edit'),
    path('pe/termimport/', pe_term.pe_term_import, name='pe_term_import'),
    path('pe/term/export/', pe_term.pe_term_export, name='pe_term_export'),
    path('pe_term/update_rank/', pe_term.pe_term_update_rank, name='pe_term_update_rank'),
    
    # 信息技术教师期中考核管理
    path('it/midlist/', it_mid.it_mid_list, name='it_mid_list'),
    path('it/midadd/', it_mid.it_mid_add, name='it_mid_add'),
    path('it/middelete/', it_mid.it_mid_delete, name='it_mid_delete'),
    path('it/midedit/<int:pk>', it_mid.it_mid_edit, name='it_mid_edit'),
    path('it/midimport/', it_mid.it_mid_import, name='it_mid_import'),
    path('it/mid/export/', it_mid.it_mid_export, name='it_mid_export'),
    path('it_mid/update_rank/', it_mid.it_mid_update_rank, name='it_mid_update_rank'),
    # 信息技术期末考核管理
    path('it/endlist/', it_end.it_end_list, name='it_end_list'),
    path('it/endadd/', it_end.it_end_add, name='it_end_add'),
    path('it/enddelete/', it_end.it_end_delete, name='it_end_delete'),
    path('it/endedit/<int:pk>', it_end.it_end_edit, name='it_end_edit'),
    path('it/endimport/', it_end.it_end_import, name='it_end_import'),
    path('it/end/export/', it_end.it_end_export, name='it_end_export'),
    path('it_end/update_rank/', it_end.it_end_update_rank, name='it_end_update_rank'),
    # 信息技术学期管理
    path('it/termlist/', it_term.it_term_list, name='it_term_list'),
    path('it/termadd/', it_term.it_term_add, name='it_term_add'),
    path('it/termdelete/', it_term.it_term_delete, name='it_term_delete'),
    path('it/termedit/<int:pk>', it_term.it_term_edit, name='it_term_edit'),
    path('it/termimport/', it_term.it_term_import, name='it_term_import'),
    path('it/term/export/', it_term.it_term_export, name='it_term_export'),
    path('it_term/update_rank/', it_term.it_term_update_rank, name='it_term_update_rank'),
    
    # 教研组长期中考核管理
    path('groupleader/midlist/', groupleader_mid.groupleader_mid_list, name='groupleader_mid_list'),
    path('groupleader/midadd/', groupleader_mid.groupleader_mid_add, name='groupleader_mid_add'),
    path('groupleader/middelete/', groupleader_mid.groupleader_mid_delete, name='groupleader_mid_delete'),
    path('groupleader/midedit/<int:pk>', groupleader_mid.groupleader_mid_edit, name='groupleader_mid_edit'),
    path('groupleader/midimport/', groupleader_mid.groupleader_mid_import, name='groupleader_mid_import'),
    path('groupleader/mid/export/', groupleader_mid.groupleader_mid_export, name='groupleader_mid_export'),
    path('groupleader_mid/update_rank/', groupleader_mid.groupleader_mid_update_rank, name='groupleader_mid_update_rank'),
    # 教研组长期期末考核管理
    path('groupleader/endlist/', groupleader_end.groupleader_end_list, name='groupleader_end_list'),
    path('groupleader/endadd/', groupleader_end.groupleader_end_add, name='groupleader_end_add'),
    path('groupleader/enddelete/', groupleader_end.groupleader_end_delete, name='groupleader_end_delete'),
    path('groupleader/endedit/<int:pk>', groupleader_end.groupleader_end_edit, name='groupleader_end_edit'),
    path('groupleader/endimport/', groupleader_end.groupleader_end_import, name='groupleader_end_import'),
    path('groupleader/end/export/', groupleader_end.groupleader_end_export, name='groupleader_end_export'),
    path('groupleader_end/update_rank/', groupleader_end.groupleader_end_update_rank, name='groupleader_end_update_rank'),
    # 教研组长期学期管理
    path('groupleader/termlist/', groupleader_term.groupleader_term_list, name='groupleader_term_list'),
    path('groupleader/termadd/', groupleader_term.groupleader_term_add, name='groupleader_term_add'),
    path('groupleader/termdelete/', groupleader_term.groupleader_term_delete, name='groupleader_term_delete'),
    path('groupleader/termedit/<int:pk>', groupleader_term.groupleader_term_edit, name='groupleader_term_edit'),
    path('groupleader/termimport/', groupleader_term.groupleader_term_import, name='groupleader_term_import'),
    path('groupleader/term/export/', groupleader_term.groupleader_term_export, name='groupleader_term_export'),
    path('groupleader_term/update_rank/', groupleader_term.groupleader_term_update_rank, name='groupleader_term_update_rank'),

    # 班主任期中考核管理
    path('headteacher/midlist/', headteacher_mid.headteacher_mid_list, name='headteacher_mid_list'),
    path('headteacher/midadd/', headteacher_mid.headteacher_mid_add, name='headteacher_mid_add'),
    path('headteacher/middelete/', headteacher_mid.headteacher_mid_delete, name='headteacher_mid_delete'),
    path('headteacher/midedit/<int:pk>', headteacher_mid.headteacher_mid_edit, name='headteacher_mid_edit'),
    path('headteacher/midimport/', headteacher_mid.headteacher_mid_import, name='headteacher_mid_import'),
    path('headteacher/mid/export/', headteacher_mid.headteacher_mid_export, name='headteacher_mid_export'),
    path('headteacher_mid/update_rank/', headteacher_mid.headteacher_mid_update_rank, name='headteacher_mid_update_rank'),
    # 班主任期末考核管理
    path('headteacher/endlist/', headteacher_end.headteacher_end_list, name='headteacher_end_list'),
    path('headteacher/endadd/', headteacher_end.headteacher_end_add, name='headteacher_end_add'),
    path('headteacher/enddelete/', headteacher_end.headteacher_end_delete, name='headteacher_end_delete'),
    path('headteacher/endedit/<int:pk>', headteacher_end.headteacher_end_edit, name='headteacher_end_edit'),
    path('headteacher/endimport/', headteacher_end.headteacher_end_import, name='headteacher_end_import'),
    path('headteacher/end/export/', headteacher_end.headteacher_end_export, name='headteacher_end_export'),
    path('headteacher_end/update_rank/', headteacher_end.headteacher_end_update_rank, name='headteacher_end_update_rank'),
    # 班主任学期考核管理
    path('headteacher/termlist/', headteacher_term.headteacher_term_list, name='headteacher_term_list'),
    path('headteacher/termadd/', headteacher_term.headteacher_term_add, name='headteacher_term_add'),
    path('headteacher/termdelete/', headteacher_term.headteacher_term_delete, name='headteacher_term_delete'),
    path('headteacher/termedit/<int:pk>', headteacher_term.headteacher_term_edit, name='headteacher_term_edit'),
    path('headteacher/termimport/', headteacher_term.headteacher_term_import, name='headteacher_term_import'),
    path('headteacher/term/export/', headteacher_term.headteacher_term_export, name='headteacher_term_export'),
    path('headteacher_term/update_rank/', headteacher_term.headteacher_term_update_rank, name='headteacher_term_update_rank'),

    # 教务员管理考核
    path('eduadmin/list/', eduadmin.eduadmin_list, name='eduadmin_list'),
    path('eduadmin/add/', eduadmin.eduadmin_add, name='eduadmin_add'),
    path('eduadmin/delete/', eduadmin.eduadmin_delete, name='eduadmin_delete'),
    path('eduadmin/edit/<int:pk>', eduadmin.eduadmin_edit, name='eduadmin_edit'),
    path('eduadmin/import/', eduadmin.eduadmin_import, name='eduadmin_import'),
    path('eduadmin/export/', eduadmin.eduadmin_export, name='eduadmin_export'),
    path('eduadmin/update_rank/', eduadmin.eduadmin_update_rank, name='eduadmin_update_rank'),
    
    # 行政后勤管理考核
    path('aladmin/list/', aladmin.aladmin_list, name='aladmin_list'),
    path('aladmin/add/', aladmin.aladmin_add, name='aladmin_add'),
    path('aladmin/delete/', aladmin.aladmin_delete, name='aladmin_delete'),
    path('aladmin/edit/<int:pk>', aladmin.aladmin_edit, name='aladmin_edit'),
    path('aladmin/import/', aladmin.aladmin_import, name='aladmin_import'),
    path('aladmin/export/', aladmin.aladmin_export, name='aladmin_export'),
    path('aladmin/update_rank/', aladmin.aladmin_update_rank, name='aladmin_update_rank'),
    
    # 副班主任管理考核
    path('deputy/list/', deputy.deputy_list, name='deputy_list'),
    path('deputy/add/', deputy.deputy_add, name='deputy_add'),
    path('deputy/delete/', deputy.deputy_delete, name='deputy_delete'),
    path('deputy/edit/<int:pk>', deputy.deputy_edit, name='deputy_edit'),
    path('deputy/import/', deputy.deputy_import, name='deputy_import'),
    path('deputy/export/', deputy.deputy_export, name='deputy_export'),
    path('deputy/update_rank/', deputy.deputy_update_rank, name='deputy_update_rank'),
]