# coding: utf-8
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ModifyPasswordForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


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
                # 用户已激活 login用户并重定向至主页
                if user.is_active:
                    login(request, user)
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
            logout(request)
            return render(request, 'index.html')


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


class ModifyPasswordView(View):
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
        return render(request, 'usercenter-info.html', {'current_user': current_user})


class UploadImageView(LoginRequiredMixin, View):
    """
        处理用户头像上传
        个人中心 - 用户个人信息 - 头像上传
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePasswordView(View):
    """个人中心修改密码"""

    def post(self, request):
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


class UpdateEmailView(View):
    """修改用户绑定邮箱"""

    def post(self, request):
        # 新邮箱地址
        new_email = request.POST.get('email', '')
        # 验证码
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=request.user.email, code=code,
                                                           new_email=new_email, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = new_email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码无效"}', content_type='application/json')