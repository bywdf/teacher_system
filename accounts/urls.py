from django.urls import path
from accounts.views import account, department, subject

app_name = 'accounts'

urlpatterns = [
    # 部门管理
    path('department/list/', department.department_list, name='department_list'),
    path('department/add/', department.department_add, name='department_add'),
    path('department/delete/', department.department_delete),
    path('department/<int:nid>/edit/', department.department_edit),
    path('department/multi/', department.department_multi),   
    
    # 学科管理
    
    # 账户管理
]