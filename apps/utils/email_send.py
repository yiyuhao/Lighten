# coding: utf-8

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Lighten.settings import EMAIL_FROM


def generate_random_str(length=8):
    """生成随机字符串  使用Random().randint()"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars_len = len(chars)
    random = Random()
    for i in xrange(length):
        str += chars[random.randint(0, chars_len-1)]
    return str


def send_register_email(email_to, send_type='register'):
    """
    发送确认邮件(注册或找回密码)
    :param email_to:       (str)    用户邮箱    '...@xx.com'
    :param send_type:      (str)    邮件类型    'register' or 'forget'
    :return:
    """
    # 随机字符串
    random_str = generate_random_str(16)

    # 实例化EmailVerifyRecord model
    email_record = EmailVerifyRecord()
    email_record.code = random_str
    email_record.email = email_to
    email_record.send_type = send_type
    email_record.save()

    # 发送邮件
    if send_type == 'register':
        email_title = 'Lighten - 注册激活'
        email_body = '请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{code}'.format(code=random_str)
        send_status = send_mail(subject=email_title,
                                message=email_body,
                                from_email=EMAIL_FROM,
                                recipient_list=[email_to])

        if send_status:
            pass
