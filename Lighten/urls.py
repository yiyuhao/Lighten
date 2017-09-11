# coding: utf-8
"""Lighten URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, \
    ForgetPasswordView, ResetPasswordView, ModifyPasswordView
from organization.views import OrgView
from Lighten.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url('^captcha/', include('captcha.urls')),
    # 邮箱激活 'active/<str active_code>'
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    # 找回密码
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forget_password'),
    # 处理重置密码的邮件链接 'reset/<str reset_code>'
    url(r'^reset/(?P<reset_code>.*)/$', ResetPasswordView.as_view(), name='reset_password'),
    # 重置密码的请求提交
    url(r'^modify_password/$', ModifyPasswordView.as_view(), name='modify_password'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 上传文件的访问处理函数
    url(r'^media/(?P<path>.*$)', serve, {'document_root': MEDIA_ROOT})
]
