from django.urls import path

from certificate.views import school_certificate


app_name = 'certificate'


urlpatterns = [
    # 校级证书基础管理
    path('shool_certificate/list/', school_certificate.school_certificate_list, name='school_certificate_list'),
    path('shool_certificate/add/', school_certificate.school_certificate_add, name='school_certificate_add'),
    path('shool_certificate/<int:nid>/edit/', school_certificate.school_certificate_edit, name='school_certificate_edit'),
    path('shool_certificate/delete/', school_certificate.school_certificate_delete, name='school_certificate_delete'),
    path('shool_certificate/multi/', school_certificate.school_certificate_multi, name='school_certificate_multi'),
    
    # 校外证书基础管理
    
    # 教师校级证管理
    
    # 教师校外证书管理
    
    # 副班主任经历管理
    
    # 年度考核管理
    
]
