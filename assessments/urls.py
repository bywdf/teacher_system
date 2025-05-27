from django.urls import path
from assessments.views import termyear

urlpatterns = [
    # 学年管理
    path('termyear/list/', termyear.termyear_list, name='termyear_list'),
    path('termyear/add/', termyear.termyear_add, name='termyear_add'),
    path('termyear/delete/', termyear.termyear_delete, name='termyear_delete'),
    path('termyear/detail/', termyear.termyear_detail, name='termyear_detail'),
    path('termyear/edit/', termyear.termyear_edit, name='termyear_edit'),
    
    # 
]