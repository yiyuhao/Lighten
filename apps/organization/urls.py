# coding: utf-8

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),

    # 用户需求: ‘我要学习’表单
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask')
]
