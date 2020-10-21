# Generated by Django 2.1.7 on 2019-09-09 20:24

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='学校名字')),
                ('cover', models.ImageField(default='', max_length=255, upload_to='orgs/schools/covers/', verbose_name='学校封面')),
                ('introduction', models.CharField(default='精勤求学，敦笃励志，果毅力行，忠恕任事', max_length=255, verbose_name='学校简介')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(default='这个学校很赖，没有详情介绍', verbose_name='学校详情')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
                ('favor_num', models.IntegerField(default=0, verbose_name='收藏量')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '学校',
                'verbose_name_plural': '学校',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='教师名字')),
                ('avatar', models.ImageField(default='', max_length=255, upload_to='orgs/teachers/avatars/', verbose_name='教师头像')),
                ('features', models.CharField(default='诙谐幽默，严谨求实', max_length=255, verbose_name='教学特色')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orgs.School', verbose_name='签约学校')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]
