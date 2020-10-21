from random import choice

from django.core.mail import send_mail


def generate_code():
    """
    生成四位数字的验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(4):
        random_str.append(choice(seeds))

    return "".join(random_str)


def send_verify_code_by_email(verifycode, to_emails):
    subject = '邮箱注册验证码'
    message = f'欢迎注册乐乎在线学习网！您的邮箱验证码是: {verifycode}'
    from_email = 'xjtuzhjm@sina.com'
    # to_emails = ['xjtuzhjm@sina.com', ]
    status = send_mail(
        subject,
        message,
        from_email,
        to_emails,
        fail_silently=False,
    )
    # 邮件发送完毕，返回发送状态
    return status


if __name__ == '__main__':
    # 独立使用django的model
    import sys
    import os

    pwd = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(pwd + "../")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LehuXuexi.settings")

    import django

    django.setup()

    # 发送邮件
    to_emails = ['xjtuzhjm@sina.com', ]
    verifycode = generate_code()
    status = send_verify_code_by_email(verifycode, to_emails)
    print(status)