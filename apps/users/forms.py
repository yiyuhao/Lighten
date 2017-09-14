# coding: utf-8
import re

from django import forms

from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    """
        登录form 参数验证

        其中参数名称如username必须和html中form表单input的name一致：
            <input name="username" id=...>
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
        注册表单 参数验证

        提供了captcha field
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetPasswordForm(forms.Form):
    """
        忘记密码
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ModifyPasswordForm(forms.Form):
    """
        修改密码
    """
    password = forms.CharField(required=True, min_length=5)
    password_repeat = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'gender', 'birthday', 'address', 'mobile']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return: None
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        if re.match(regex_mobile, mobile):
            return mobile
        else:
            raise forms.ValidationError(u'无效的手机号码', code='mobile_invalid')