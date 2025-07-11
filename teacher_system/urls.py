"""
URL configuration for teacher_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import account
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 首页
    path('', account.index, name='index'),
    
    # 后台管理
    path('admin/', admin.site.urls),
    
    # 登录注销
    path('image/code/', account.image_code, name='image_code'),
    path("login/", account.user_login, name="login"),
    path("logout/", account.user_logout, name="logout"),
    
    # 路由分发
    path('accounts/', include('accounts.urls')),
    path('assessments/', include('assessments.urls')),
]

# 仅在开发环境中添加此配置,生产环境由Nginx处理
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
