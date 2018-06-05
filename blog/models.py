from __future__ import unicode_literals

import time

from django.db import models
from django.contrib.auth import get_user_model
from .base_model import BaseModel


class Category(BaseModel):
    name = models.CharField('分类名称', max_length=31)
    display_order = models.IntegerField('分类排序', default=999)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField('标签名称', max_length=30)
    display_order = models.IntegerField('标签排序', default=999)
    color = models.CharField('标签颜色', max_length=10, default='#FFE9DC')

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.name


def image_upload_to(filename):
    """文章图存储位置"""
    suffix = filename.split('.')[-1]
    return 'blog/article/{0}'.format(str(time.time()) + '.' + suffix)


class Article(BaseModel):
    STATUS_CHOICES = (
        ('PART', '未发布'),
        ('PUBLISHED', '已发布'),
    )
    user = models.ForeignKey(get_user_model(), verbose_name='用户')
    category = models.ForeignKey(Category, verbose_name='所属分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签', null=True, blank=True, help_text='标签id可以对应多个')
    title = models.CharField('标题', max_length=255)
    description = models.CharField('描述/摘要', max_length=255, null=False, blank=False)
    views = models.PositiveIntegerField('访问量', default=0)
    img = models.ImageField('文章图片', upload_to=image_upload_to)
    article = models.TextField('文章')
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)
    status = models.CharField('文章状态', max_length=10, choices=STATUS_CHOICES)
    display_order = models.IntegerField('标签排序', default=999)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["display_order", 'pk']

    def __unicode__(self):
        return self.title


class Comments(BaseModel):
    name = models.CharField('姓名', max_length=30)
    email = models.EmailField(null=True, blank=True)
    article = models.ForeignKey(Article, verbose_name='文章')
    comment = models.ForeignKey('self',  verbose_name='被回复的评论', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField('评论内容')

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name + str(self.created_at)


class Suggest(BaseModel):
    """
    意见存储
    """
    name = models.CharField('姓名', max_length=30)
    email = models.EmailField(null=True, blank=True)
    suggest = models.TextField('意见', max_length=300)

    def __str__(self):
        return self.suggest
