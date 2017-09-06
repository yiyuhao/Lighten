# coding: utf-8
import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "Lighten后台管理"
    site_footer = 'Lighten'
    menu_style = 'accordion'


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
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)