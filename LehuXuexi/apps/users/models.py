from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UserProfile(AbstractUser):
    """
    用户
    """
    nickname = models.CharField(max_length=20, null=True, blank=True, verbose_name="昵称")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    email = models.CharField(max_length=125, null=True, blank=True, verbose_name="邮箱")
    introduction = models.TextField(blank=True, null=True, verbose_name='简介', default='该用户很懒，啥也没写...')
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='头像', default='')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='用户住址', default='')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True, default=timezone.now)
    gender = models.CharField(verbose_name='性别', choices=(('male', '男'), ('female', '女')), max_length=6, default=
                              'male')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username


class VerifyCode(models.Model):
    """
    短信或邮箱验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码", default='')
    account = models.CharField(max_length=125, verbose_name="账号", default='')
    account_type = models.CharField(verbose_name="账号类型", choices=(("email", "邮箱"), ("mobile", "手机")),
                                    default='email', max_length=6)
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
