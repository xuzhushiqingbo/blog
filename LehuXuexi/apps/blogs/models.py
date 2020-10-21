from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BlogCategory(models.Model):
    """
    博客分类类目
    """
    name = models.CharField(max_length=30, verbose_name="类别名", help_text="类别名")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "博客类别"
        verbose_name_plural = verbose_name
        ordering = ('add_time',)

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    """
    博客分类标签
    """
    name = models.CharField(max_length=25, verbose_name='标签名称')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name
        ordering = ('add_time',)


class Article(models.Model):
    """博客文章"""
    category = models.ForeignKey(BlogCategory, verbose_name="文章类别", null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(BlogTag, blank=True, verbose_name="文章标签")
    user = models.ForeignKey(User, verbose_name='文章作者', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='文章标题')
    brief = models.CharField(max_length=255, verbose_name='文章摘要', default='这篇文章没有摘要', blank=True)
    cover = models.ImageField(upload_to='blogs/articles/covers/', verbose_name='文章封面', max_length=255, null=True,
                              blank=True)
    content = models.TextField(verbose_name='文章内容')
    click_num = models.IntegerField(verbose_name='点击量', default=0)
    favor_num = models.IntegerField(verbose_name='收藏量', default=0)
    comment_num = models.IntegerField(verbose_name='评论量', default=0)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name
        ordering = ('add_time', )


class ArticleImage(models.Model):
    """文章插图"""
    image = models.ImageField(upload_to='blogs/articles/content/', verbose_name='文章插图', max_length=255, null=True,
                              blank=True)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    def __str__(self):
        return self.image

    class Meta:
        verbose_name = '文章插图'
        verbose_name_plural = verbose_name
        ordering = ('-add_time', )
