from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name='学校名字')
    cover = models.ImageField(upload_to="orgs/schools/covers/", verbose_name="学校封面", max_length=255, default='')
    introduction = models.CharField(max_length=255, verbose_name="学校简介", default='精勤求学，敦笃励志，果毅力行，忠恕任事')
    description = RichTextUploadingField(verbose_name="学校详情", default='这个学校很赖，没有详情介绍')
    click_num = models.IntegerField(verbose_name='点击量', default=0)
    favor_num = models.IntegerField(verbose_name='收藏量', default=0)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    school = models.ForeignKey(School, verbose_name="签约学校", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25, verbose_name='教师名字')
    avatar = models.ImageField(default='', upload_to="orgs/teachers/avatars/", verbose_name="教师头像", max_length=255)
    features = models.CharField(max_length=255, verbose_name="教学特色", default='诙谐幽默，严谨求实')

    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
