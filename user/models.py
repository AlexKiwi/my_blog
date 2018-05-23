from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Sex(object):
    MALE = "1"
    FEMALE = "2"
    UNKNOWN = "0"
    Choices = ((MALE, '男性'), (FEMALE, '女性'), (UNKNOWN, '未知'))


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name='用户')
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="user/avatars", max_length=100, verbose_name="头像")
    sex = models.CharField(max_length=1, choices=Sex.Choices, defaul=0, verbose_name="性别")

    class Meta:
        verbose_name = "用户补充"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.user.id) + '  ' + str(self.nickname)

