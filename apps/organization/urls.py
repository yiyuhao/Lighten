# coding: utf-8

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView, \
    OrgDetailHomepageView, OrgDetailCourseView, OrgDetailDescView, OrgDetailTeacherView, AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    # 授课机构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),

    # 用户需求: ‘我要学习’表单
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),

    # 首页->课程机构->机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgDetailHomepageView.as_view(), name='org_home'),
    # 首页->课程机构->机构课程
    url(r'^course/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name='org_course'),
    # 首页->课程机构->机构介绍
    url(r'^desc/(?P<org_id>\d+)/$', OrgDetailDescView.as_view(), name='org_desc'),
    # 首页->课程机构->机构讲师(列表)
    url(r'^teacher/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 讲师详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
