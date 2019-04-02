# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
import os
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from users.models import ExtraProfile
# Create your models here.



def get_image_path(instance, filename):
    return os.path.join('img/course', str(instance.id), filename)
    
def get_courseHw_image_path(instance, filename):
    return os.path.join('course/homework', str(instance.id), '/demo/',filename)
    
def get_courseResource_image_path(instance, filename):
    return os.path.join('course/resource', str(instance.course_id), filename)
    
def get_sh_path(instance, filename):
    return os.path.join('course/homework', str(instance.course_id), filename)
    
def timeLimitSet():
    return datetime.now()+timedelta(days=7)


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"課程名")
    desc = models.CharField(max_length=300, verbose_name=u"課程描述")
    detail = models.TextField(verbose_name=u"課程詳情")
    instructor = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"指導老師")
    image = models.ImageField(upload_to=get_image_path, default='img/course/default_course.jpg', blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")

    class Meta:
        verbose_name = u"課程"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"課程")
    name = models.CharField(max_length=100, verbose_name=u"名稱")
    detail = models.TextField(verbose_name=u"文件描述", blank=True, null=True)
    download = models.FileField(upload_to=get_courseResource_image_path, blank=True, null=True, verbose_name=u"資源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"課程資源"
        verbose_name_plural = verbose_name
        
class CourseHomework(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"課程")
    name = models.CharField(max_length=100, verbose_name=u"標題")
    desc = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"描述")
    detail = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"內容")
    uploadFile = models.FileField(upload_to=get_courseHw_image_path, blank=True, null=True, verbose_name=u"範例檔案")
    deadline_token = models.CharField(max_length=1, choices=(("0",u"否"),("1",u"是")), default=u"0", verbose_name=u"是否到期")
    limit_time = models.DateTimeField(default=timeLimitSet ,verbose_name=u"繳交時間")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"課程作業"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.name


class StudentHomework(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"課程")
    homework = models.ForeignKey(CourseHomework, verbose_name=u"作業")
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    file = models.FileField(upload_to=get_sh_path, blank=True, null=True, verbose_name=u"檔案")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"學生作業上傳"
        verbose_name_plural = verbose_name
        
    def filename(self):
        return os.path.basename(self.file.name)




class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"課程")
    name = models.CharField(max_length=100, verbose_name=u"章節名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"章節"
        verbose_name_plural = verbose_name