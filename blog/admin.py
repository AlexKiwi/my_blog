# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.Comments)
admin.site.register(models.Suggest)
