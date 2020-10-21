from django.contrib import admin

from .models import UserProfile, VerifyCode


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'mobile', 'is_staff', 'is_active']


admin.site.register(UserProfile, UserProfileAdmin)


class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'account', 'account_type', 'add_time']


admin.site.register(VerifyCode, VerifyCodeAdmin)

