from django.contrib import admin

from .models import School, Teacher


class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'click_num', 'favor_num', 'add_time']


admin.site.register(School, SchoolAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school', 'features', 'add_time']


admin.site.register(Teacher, TeacherAdmin)
