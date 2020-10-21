# Generated by Django 2.1.7 on 2019-10-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191005_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=6, verbose_name='性别'),
        ),
    ]