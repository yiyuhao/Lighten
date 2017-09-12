# coding: utf-8

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView


urlpatterns = [
    # 课程详情页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程列表页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    # 课程视频页(开始学习)
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='info'),
]
