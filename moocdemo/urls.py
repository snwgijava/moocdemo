"""moocdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from users import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('org/',include('organization.urls'),name='org'),
    #首页
    path('',TemplateView.as_view(template_name='index.html'),name='index'),
    #登录
    path('login/',views.LoginView.as_view(),name='login'),
    #注册
    path('register/',views.RegisterView.as_view(),name='register'),
    #激活用户
    path('active/<str:active_code>/',views.ActiveUserView.as_view(),name='user_active'),
    #忘记密码
    path('forget/',views.ForgetPwdView.as_view(),name='forget_pwd'),
    #重置密码
    path('reset/<str:active_code>/',views.ResetView.as_view(),name='reset_pwd'),
    #修改密码
    path('modify_pwd/',views.ModifyPwdView.as_view(),name='modify_pwd'),
    #验证码
    path('captcha/',include('captcha.urls')),
    #处理图片的url   处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT }),

]
