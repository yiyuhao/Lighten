# coding: utf-8
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ModifyPasswordForm, UploadImageForm, UserInfoForm
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from pure_pagination import PageNotAnInteger, Paginator
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from Lighten.settings import PAGINATION_SETTINGS


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None


class LoginView(View):
    """用户登录"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 尝试认证用户并返回user
            user = authenticate(username=username, password=password)
            if user:
                user.log('尝试登录Lighten')
                # 用户已激活 login用户并重定向至主页
                if user.is_active:
                    login(request, user)
                    user.log('成功登录Lighten')
                    return render(request, 'index.html')
                # 用户未激活 返回提示信息
                return render(request, 'login.html', {'msg': '请前往邮箱激活'})
            # 用户名密码错误
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        # 表单字段未验证通过
        return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        request.user.log('退出登录')
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            # 邮箱是否已被注册
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html',
                              {'msg': '该邮箱已被注册', 'register_form': register_form})
            password = request.POST.get('password', '')
            # 初始化注册用户信息
            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()
            user.log('欢迎注册Lighten-中国成都市龙泉驿区北泉路最大的的在线教育网站')
            # 发送注册邮件
            send_register_email(email, 'register')
            return render(request, 'login.html')
        else:
            # 表单字段未验证通过
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    """用户邮箱激活"""

    def get(self, request, active_code):
        email_verify_records = EmailVerifyRecord.objects.filter(code=active_code)
        if email_verify_records:
            for record in email_verify_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
                user.log('你已激活')
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ForgetPasswordView(View):
    """找回密码界面(输入邮箱获取确认邮件)"""

    def get(self, request):
        forget_form = ForgetPasswordForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPasswordForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPasswordView(View):
    """处理用户重置密码的链接"""

    def get(self, request, reset_code):
        email_verify_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if email_verify_records:
            for record in email_verify_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


class ModifyPasswordView(LoginRequiredMixin, View):
    """提供表单给用户修改密码(忘记密码)"""

    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        email = request.POST.get('email', '')

        if modify_form.is_valid():
            password = request.POST.get('password', '')
            password_repeat = request.POST.get('password_repeat', '')
            # 验证两次密码输入一致
            if password != password_repeat:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            # 更新用户密码
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            user.log('(通过邮箱验证)重置了密码')
            # 密码修改成功, 返回登录界面
            return render(request, 'login.html')
        return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


# ###################个人中心View################### #
class UserInfoView(LoginRequiredMixin, View):
    """
        个人中心 - 用户个人信息
    """

    def get(self, request):
        current_user = request.user
        # current_user = UserProfile()
        return render(request, 'usercenter-info.html', {'current_user': current_user})

    def post(self, request):
        """修改用户信息"""

        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            request.user.log('修改了个人信息')
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
        处理用户头像上传
        个人中心 - 用户个人信息 - 头像上传
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            request.user.log('修改了头像')
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePasswordView(LoginRequiredMixin, View):
    """个人中心修改密码"""

    def post(self, request):
        request.user.log('尝试修改密码')
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            password = request.POST.get('password', '')
            password_repeat = request.POST.get('password_repeat', '')
            # 验证两次密码输入一致
            if password != password_repeat:
                return HttpResponse('{"status": "fail", "msg": "密码不一致"}',
                                    content_type='application/json')
            # 更新用户密码
            user = request.user
            user.password = make_password(password)
            user.save()
            user.log('成功修改密码')
            logout(request)
            # 密码修改成功, 返回登录界面
            return HttpResponse('{"status": "success"}', content_type='application/json')
        return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱验证"""

    def get(self, request):
        new_email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=new_email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')
        send_register_email(email_to=request.user.email, send_type='update_email',
                            user_new_email=new_email)
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改用户绑定邮箱"""

    def post(self, request):
        request.user.log('尝试修改绑定邮箱')
        # 新邮箱地址
        new_email = request.POST.get('email', '')
        # 验证码
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=request.user.email, code=code,
                                                           new_email=new_email, send_type='update_email')
        if existed_records:
            user = request.user
            user.log('绑定邮箱已由{old_email}修改为{new_email}'.format(old_email=user.email, new_email=new_email))
            user.email = new_email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """我的课程"""

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'user_courses': user_courses})


class FavOrgView(LoginRequiredMixin, View):
    """收藏机构"""

    def get(self, request):
        # (1, u'课程'), (2, u'课程机构'), (3, u'讲师')
        fav_records = UserFavorite.objects.filter(user=request.user, fav_type=2)
        user_fav_orgs = []
        for i in fav_records:
            user_fav_orgs.append(CourseOrg.objects.get(id=i.fav_id))
        return render(request, 'usercenter-fav-org.html', {'user_fav_orgs': user_fav_orgs})


class FavTeacherView(LoginRequiredMixin, View):
    """收藏教师"""

    def get(self, request):
        # (1, u'课程'), (2, u'课程机构'), (3, u'讲师')
        fav_records = UserFavorite.objects.filter(user=request.user, fav_type=3)
        user_fav_teachers = []
        for i in fav_records:
            user_fav_teachers.append(Teacher.objects.get(id=i.fav_id))
        return render(request, 'usercenter-fav-teacher.html', {'user_fav_teachers': user_fav_teachers})


class FavCourseView(LoginRequiredMixin, View):
    """收藏课程"""

    def get(self, request):
        # (1, u'课程'), (2, u'课程机构'), (3, u'讲师')
        fav_records = UserFavorite.objects.filter(fav_type=1)
        user_fav_courses = []
        for i in fav_records:
            user_fav_courses.append(Course.objects.get(id=i.fav_id))
        return render(request, 'usercenter-fav-course.html', {'user_fav_courses': user_fav_courses})


class UserMessageView(LoginRequiredMixin, View):
    """用户消息"""

    def get(self, request):
        # UserMessage.user == 0 代表全体消息
        messages = UserMessage.objects.filter(Q(user=request.user.id) | Q(user=0)).order_by('-add_time')

        # 所有消息标为已读
        for msg in messages:
            msg.has_read = True
            msg.save()

        # 对消息进行分页
        per_page = PAGINATION_SETTINGS.get('MESSAGE_NUM_PER_PAGE', 10)
        p = Paginator(messages, per_page, request=request)
        try:
            page_num = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page_num = 1
        messages_paginator = p.page(page_num)

        return render(request, 'usercenter-message.html', {'messages_paginator': messages_paginator})