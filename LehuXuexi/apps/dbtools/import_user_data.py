# -*- coding: utf-8 -*-

__author__ = 'antares'

# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LehuXuexi.settings")

import django

django.setup()

users_data = [
    {
        'username': 'admin',
        'nickname': '管理员',
        'mobile': '15002959010',
        'email': 'admin@lehu.com',
        "avatar": "users/avatars/0.jpg",
        "is_superuser": True,
        "is_staff": True,
        "is_active": True
    },
    {
        'username': 'weixiaobao',
        'nickname': '韦小宝',
        'mobile': '15002959011',
        'email': 'weixiaobao@lehu.com',
        "avatar": "users/avatars/1.jpg",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True
    },
    {
        'username': 'zhaochunhua',
        'nickname': '赵春花',
        'mobile': '15002959012',
        'email': 'zhaochunhua@lehu.com',
        "avatar": "users/avatars/2.jpg",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True
    },
    {
        'username': 'yangliuzhi',
        'nickname': '杨柳枝',
        'mobile': '15002959013',
        'email': 'yangliuzhi@lehu.com',
        "avatar": "users/avatars/3.jpg",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True
    },
    {
        'username': 'zhangxiaotian',
        'nickname': '张笑天',
        'mobile': '15002959014',
        'email': 'zhangxiaotian@lehu.com',
        "avatar": "users/avatars/4.jpg",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True
    },
    {
        'username': 'yuanhaowen',
        'nickname': '元好问',
        'mobile': '15002959015',
        'email': 'yuanhaowen@lehu.com',
        "avatar": "users/avatars/5.jpg",
        "is_superuser": False,
        "is_staff": False,
        "is_active": True
    },
]

from users.models import UserProfile
from django.contrib.auth.hashers import make_password

for item in users_data:
    if not UserProfile.objects.filter(username=item['username']).first():
        user = UserProfile(**item)
        user.password = make_password('123456789')
        user.save()
        print(user.id, '---', user.password)
    else:
        print(item['username'], '用户名已经存在了！')
