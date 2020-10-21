from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone

from orgs.models import School, Teacher


class CourseCategory(models.Model):
    """
    课程分类类目
    """
    CATEGORY_TYPE = ((1, "一级类目"), (2, "二级类目"), (3, "三级类目"))
    name = models.CharField(max_length=30, verbose_name="类别名称", help_text="类别名称")
    code = models.CharField(max_length=30, verbose_name="类别代码", help_text="类别代码")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent = models.ForeignKey("self", null=True, blank=True, verbose_name="父级类目", help_text="父级类目",
                               related_name="children", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(CourseCategory, verbose_name="课程类别", null=True, blank=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, verbose_name="授课机构", null=True, blank=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Teacher, verbose_name="授课教师", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=125, verbose_name='课程名称')
    degree = models.CharField(verbose_name="课程难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    introduction = models.CharField(max_length=255, verbose_name='课程简介', default='这个课程没有简介')
    description = RichTextUploadingField(verbose_name='课程描述')
    cover = models.ImageField(upload_to='courses/courses/covers/', verbose_name='课程封面', max_length=255, null=True,
                              blank=True)
    recommend = models.CharField(verbose_name='推荐', choices=(("yes", "推荐到首页"), ("no", "不推荐到首页")), max_length=3)
    click_num = models.IntegerField(verbose_name='点击量', default=0)
    favor_num = models.IntegerField(verbose_name='收藏量', default=0)
    comment_num = models.IntegerField(verbose_name='评论量', default=0)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
