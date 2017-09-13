# coding: utf-8

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, CourseVideoView


urlpatterns = [
    # 课程详情页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程列表页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),
    # 课程视频页(开始学习)
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='info'),
    # 课程评论页(开始学习)
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='comment'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    # 课程视频播放
    url(r'^video/(?P<video_id>\d+)/$', CourseVideoView.as_view(), name='video_play'),
]
