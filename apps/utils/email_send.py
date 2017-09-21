# coding: utf-8

from random import Random
from threading import Thread

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Lighten.settings import EMAIL_FROM


def generate_random_str(length=8):
    """生成随机字符串  使用Random().randint()"""
    str = ''
    # (用户验证码输入体验)去掉 Ii Ll 11 Oo0
    chars = 'AaBbCcDdEeFfGgHhJjKkMmNnPpQqRrSsTtUuVvWwXxYyZz23456789'
    chars_len = len(chars)
    random = Random()
    for i in xrange(length):
        str += chars[random.randint(0, chars_len - 1)]
    return str


def async_send_email(*args, **kwargs):
    """Multi Thread发送邮件"""
    th = Thread(target=send_mail, name='send email', args=args, kwargs=kwargs)
    th.start()


def send_register_email(email_to, send_type='register', user_new_email='', host='127.0.0.1:8000'):
    """
    发送确认邮件(注册或找回密码)
    :param email_to:         (str)   用户邮箱    '...@xx.com'
    :param send_type:        (str)   邮件类型    'register' 'forget' or 'update_email'
    :param user_new_email:   (str)   用户更新邮箱时的参数, 告诉用户将要修改的邮箱地址
    :param host:             (str)   主机地址, 写入链接提供给用户
    :return:
    """
    # 随机字符串
    random_str = generate_random_str(16) if not user_new_email else generate_random_str(4)

    # 实例化EmailVerifyRecord model
    email_record = EmailVerifyRecord()
    email_record.code = random_str
    email_record.email = email_to
    email_record.new_email = user_new_email
    email_record.send_type = send_type
    email_record.save()

    # 发送邮件
    if send_type == 'register':
        email_title = 'Lighten - 注册激活'
        email_body = '请点击下面的链接激活你的账号: ' \
                     'http://{host}/active/{code}'.format(host=host, code=random_str)

    elif send_type == 'forget':
        email_title = 'Lighten - 密码重置'
        email_body = '请点击下面的链接重置你的密码: ' \
                     'http://{host}/reset/{code}'.format(host=host, code=random_str)

    elif send_type == 'update_email':
        email_title = 'Lighten - 邮箱修改验证码'
        email_body = '你正在修改Lighten账号的绑定邮箱为{email}，请确认是本人的操作。' \
                     '验证码为: {code}'.format(email=user_new_email, code=random_str)

    async_send_email(subject=email_title,
                     message=email_body,
                     from_email=EMAIL_FROM,
                     recipient_list=[email_to])
