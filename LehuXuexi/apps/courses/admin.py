from django.contrib import admin

from .models import CourseCategory, Course


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'add_time']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',  'category',  'school',  'teacher',  'degree', 'add_time']


admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
