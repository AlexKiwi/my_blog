from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)
    deleted_at = models.DateTimeField("删除时间", null=True, blank=True, default=None)

    # 没有这个不可以继承
    class Meta:
        abstract = True

    def logical_delete(self):
        self.deleted_at = timezone.now()
        self.save()
