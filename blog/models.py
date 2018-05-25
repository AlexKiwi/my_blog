from __future__ import unicode_literals

import time
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=31, verbose_name='分类名称')
    display_order = models.IntegerField(default=999, verbose_name='分类排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "产品分类"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    display_order = models.IntegerField(default=999, verbose_name='标签排序')
    color = models.CharField(max_length=10, default='#FFE9DC', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.name


def image_upload_to(instance, filename):
    """文章图存储位置"""
    suffix = filename.split('.')[-1]
    return 'blog/article/{0}'.format(str(time.time()) + '.' + suffix)


class Article(models.Model):
    category = models.ForeignKey(Category, verbose_name='所属分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    title = models.CharField(max_length=255, verbose_name='标题')
    description = models.CharField(max_length=255, verbose_name='描述')
    views = models.IntegerField(default=0, verbose_name='访问量')
    img = models.ImageField(upload_to=image_upload_to, verbose_name='文章图片')
    article = models.TextField('文章')
    display_order = models.IntegerField(default=999, verbose_name='标签排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='用户')
    article = models.ForeignKey(Article, verbose_name='文章')
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='被回复的评论')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user + self.created_at
