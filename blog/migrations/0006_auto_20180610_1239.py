# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-10 04:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180610_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_top',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='top_comments', to='blog.Comments', verbose_name='楼主评论'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Comments', verbose_name='被回复的评论'),
        ),
    ]
