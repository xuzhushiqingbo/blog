# Generated by Django 2.1.7 on 2019-10-05 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_verifycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifycode',
            name='account',
            field=models.CharField(default='', max_length=125, verbose_name='账号'),
        ),
        migrations.AddField(
            model_name='verifycode',
            name='account_type',
            field=models.CharField(choices=[('email', '邮箱'), ('mobile', '手机')], default='email', max_length=6, verbose_name='账号类型'),
        ),
    ]
