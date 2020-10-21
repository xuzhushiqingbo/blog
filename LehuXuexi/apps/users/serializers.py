import datetime
import re
import time

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from LehuXuexi.settings import REGEX_MOBILE
from users.models import UserProfile, VerifyCode

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'nickname', 'avatar']


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'mobile', 'email', 'nickname', 'avatar', 'introduction', 'address', 'birthday',
                  'gender']


class VerifyCodeSerializer(serializers.ModelSerializer):
    account_type = serializers.ChoiceField(label='账号类型', choices=(("email", "邮箱"), ("mobile", "手机")), help_text='账号类型')
    account = serializers.CharField(label='账号', max_length=125, help_text='账号')

    # def validate_account(self, account):
    #     print(account)
    #     pass

    def validate(self, attrs):
        accountType = attrs['account_type']
        account = attrs['account']
        # 账号是否被注册过
        if UserProfile.objects.filter(Q(mobile=account) | Q(email=account)).first():
            raise serializers.ValidationError("用户账号已经存在")
        if accountType == 'mobile':
            # 验证手机号码是否合法
            if not re.match(REGEX_MOBILE, account):
                raise serializers.ValidationError("手机号码非法")

        return attrs

    class Meta:
        model = VerifyCode
        fields = ['account_type', 'account']


class UserRegSerializer(serializers.ModelSerializer):
    """用户注册的序列化"""
    account_type = serializers.ChoiceField(required=True, write_only=True, label='账号类型', choices=(("email", "邮箱"), ("mobile", "手机")),
                                           help_text='账号类型')
    account = serializers.CharField(required=True, write_only=True, label='账号', max_length=125, help_text='账号',
                                    error_messages={'blank': "请输入账号", 'required': '账号是必填项'},)
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={'blank': "请输入验证码", 'required': '验证码是必填项'},
                                 help_text='验证码')

    def validate_code(self, code):
        account_type = self.initial_data['account_type']
        account = self.initial_data['account']
        existed = VerifyCode.objects.filter(account_type=account_type, account=account).order_by('-add_time')
        if existed:
            last_record = existed[0]
            five_mintes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=20, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("账号不存在")

    def validate(self, attrs):
        accountType = attrs['account_type']
        if accountType == 'email':
            attrs['email'] = attrs['account']
        if accountType == 'mobile':
            attrs['mobile'] = attrs['account']
        attrs['nickname'] = attrs['username']
        from django.contrib.auth.hashers import make_password
        attrs['password'] = make_password(attrs['password'])
        del attrs['code']
        del attrs['account_type']
        del attrs['account']
        return attrs

    class Meta:
        model = UserProfile
        fields = ['account_type', 'account', 'code', 'username', 'password']
