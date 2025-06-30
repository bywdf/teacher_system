from django.urls import path
from accounts.views import user, department, subject, account

app_name = 'accounts'

urlpatterns = [
    # 验证管理
    # path('check_code/',account.check_code_view, name='check_code'),
    
    # 用户管理
    path('user/list/', user.user_list, name='user_list'),
    path('user/add/', user.user_add, name='user_add'),
    path('user/delete/', user.user_delete, name='user_delete'),
    path('user/<int:nid>/edit/', user.user_edit, name='user_edit'),
    path('user/import/', user.import_users, name='import_users'),
    path('user/<int:nid>/reset/', user.user_reset, name='user_reset'),
    
    # 部门管理
    path('department/list/', department.department_list, name='department_list'),
    path('department/add/', department.department_add, name='department_add'),
    path('department/delete/', department.department_delete, name='department_delete'),
    path('department/<int:nid>/edit/', department.department_edit, name='department_edit'),
    path('department/multi/', department.department_multi, name='department_multi'),

    # 学科管理
    path('subject/list/', subject.subject_list, name='subject_list'),
    path('subject/add/', subject.subject_add, name='subject_add'),
    path('subject/delete/', subject.subject_delete, name='subject_delete'),
    path('subject/edit/', subject.subject_edit, name='subject_edit'),
    path('subject/detail/', subject.subject_detail, name='subject_detail'),
    path('subject/multi/', subject.subject_multi, name='subject_multi'),    
]