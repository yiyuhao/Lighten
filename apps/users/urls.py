# coding: utf-8

from django.conf.urls import url

from .views import UserInfoView

urlpatterns = [
    # 用户信息
    url(r'^list$', UserInfoView.as_view(), name='user_info')
]