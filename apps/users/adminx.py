# coding: utf-8
import xadmin

from .models import UserProfile, EmailVerifyRecord, Banner


# class UserProfileAdmin(object):
#     fields = ['nickname', 'birthday', 'gender', 'address', 'mobile', 'image', 'add_time']
#     list_display = fields
#     list_filter = fields
#     search_fields = fields[:]
#     search_fields.remove('add_time')


class EmailVerifyRecordAdmin(object):
    fields = ['code', 'email', 'send_type', 'send_time']
    list_display = fields
    list_filter = fields
    search_fields = fields[:]
    search_fields.remove('send_time')


class BannerAdmin(object):
    fields = ['title', 'image', 'url', 'index', 'add_time']
    list_display = fields
    list_filter = fields
    search_fields = fields[:]
    search_fields.remove('add_time')

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
