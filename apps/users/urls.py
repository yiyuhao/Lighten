# coding: utf-8

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePasswordView

urlpatterns = [
    # 用户信息
    url(r'^list$', UserInfoView.as_view(), name='user_info'),

    # 处理用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='upload_image'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePasswordView.as_view(), name='update_pwd')
]