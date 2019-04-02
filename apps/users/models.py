# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


def get_image_path(instance, filename):
    return os.path.join('img/user', str(instance.user.id), filename)

class ExtraProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True , verbose_name=u'使用者')
    name = models.CharField(max_length=50, default=" ", verbose_name=u'學號')
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female",u"女")), default=u"male")
    identify = models.CharField(max_length=7, choices=(("teacher",u"老師"),("student",u"學生")), default=u"學生", verbose_name="身份")
    image = models.ImageField(upload_to=get_image_path, default='img/user/default_user.png', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"使用者額外資訊"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.name