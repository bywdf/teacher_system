from django.contrib import admin

from .models import UserInfo
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'department', 'subject', 'phone')
    search_fields = (
        'username',
        'name',
        'phone',
        'idnumber',
        'department__title',  # 如果 Department 有 name 字段
        'subject__title',      # 如果 Subject 有 name 字段
    )
    list_filter = ('gender', 'department', 'subject', 'professional_title')
    ordering = ('-date_joined',)