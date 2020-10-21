# -*- coding: utf-8 -*-
from random import randint, choice

__author__ = 'antares'

# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LehuXuexi.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

from blogs.models import BlogCategory, BlogTag, Article

# 标签数据
tags_data = ['python', 'java', 'nodejs', 'javascript', 'html', 'css', 'julia', 'matlab', 'go', 'c++', 'linux', 'mysql',
             'mongodb', 'vue', 'react', 'django', 'flask', 'tornado', 'latex', 'word', 'pyramid', 'excel', 'bigdata']

for tag_name in tags_data:
    if not BlogTag.objects.filter(name=tag_name).first():
        tag = BlogTag()
        tag.name = tag_name
        tag.save()
        print(tag.id, ' ---> ', tag.name)
    else:
        print(tag_name, '已经存在')


# 导入博客类别数据
categories_data = ['Web开发', '人工智能', '天文地理', '环球政治', '人文社科', '动物世界', '道德观察', '财税金融']

for ctg_name in categories_data:
    if not BlogCategory.objects.filter(name=ctg_name).first():
        category = BlogCategory()
        category.name = ctg_name
        category.save()
        print(category.id, ' ---> ', category.name)
    else:
        print(ctg_name, '已经存在')

# 导入文章数据
article_content = []
with open('./articles1-richeditor.html', 'r', encoding='UTF-8') as f:
    article_content.append(f.read())
with open('./articles2-richeditor.html', 'r', encoding='UTF-8') as f:
    article_content.append(f.read())
print(article_content)

article_titles = []
with open('./article_titles.txt', 'rb') as f:
    lines = f.readlines()
    for item in lines:
        article_titles.append(item.decode('utf8').rstrip(',\r\n'))
print(article_titles)
print(len(article_titles))

loop = 0
for title in article_titles:
    existed = Article.objects.filter(title=title).first()
    if existed:
        existed.content = choice(article_content)
        existed.save()
    else:
        loop += 1
        article = Article()
        article.title = title
        article.brief = "别人当他敌人，他却又当敌人是朋友，他永远坚持自己的信条，但在处理具体事物时，又不乏灵活的手腕。"
        article.content = choice(article_content)
        article.click_num = randint(10, 100)
        article.favor_num = randint(10, 100)
        article.comment_num = randint(10, 100)
        article.category = choice(BlogCategory.objects.all())
        article.user = choice(User.objects.all())
        article.cover = "blogs/articles/covers/" + str(loop % 40 + 1) + '.jpg'
        article.save()
        print(article.id)
