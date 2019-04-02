# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
import os
from django.conf import settings
from datetime import datetime

from django.db import models

from users.models import ExtraProfile
from courses.models import Course

# Create your models here.


# Add this method to your model
def audio_file_player(self):
    """audio player tag for admin"""
    if self.audio_file:
        file_url = settings.MEDIA_URL + str(self.audio_file)
        player_string = '<ul class="playlist"><li style="width:250px;">\
        <a href="%s">%s</a></li></ul>' % (file_url, os.path.basename(self.audio_file.name))
        return player_string

def get_sound_path(instance,filename):
    return os.path.join('sound/', str(instance.course_id),filename)



###
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手機")
    course_name = models.CharField(max_length=50, verbose_name=u"課程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"用戶諮詢"
        verbose_name_plural = verbose_name




#留言板
class CourseComments(models.Model):
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    course = models.ForeignKey(Course, verbose_name=u"課程")
    comment = models.CharField(max_length=200, verbose_name=u"評論")
    like = models.IntegerField(default=0, verbose_name=u"讚數")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"位置")
    picture = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"圖檔位置")
    video = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"影片檔位置")
    sound = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"聲音檔位置")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"討論區的評論"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.comment
        
        
class CommentComment(models.Model):
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    title = models.ForeignKey(CourseComments, verbose_name=u"討論主題")
    comment = models.CharField(max_length=200, verbose_name=u"回覆內容")
    like = models.IntegerField(default=0, verbose_name=u"讚數")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"評論底下的回覆"
        verbose_name_plural = verbose_name
        
        
#讚數table

class CommentPostLike(models.Model):
    title = models.ForeignKey(CourseComments, verbose_name=u"討論主題")
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"評論讚數"
        verbose_name_plural = verbose_name

        
class ReplyPostLike(models.Model):
    title = models.ForeignKey(CommentComment, verbose_name=u"回覆主題")
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"回覆讚數"
        verbose_name_plural = verbose_name


###
    

class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用戶")
    message = models.CharField(max_length=500, verbose_name=u"消息內容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已讀")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"用戶消息"
        verbose_name_plural = verbose_name
        
        
class UserCourse(models.Model):
    user = models.ForeignKey(ExtraProfile, verbose_name=u"用戶")
    course = models.ForeignKey(Course, verbose_name=u"課程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加時間")
    
    class Meta:
        verbose_name = u"用戶所選的課程"
        verbose_name_plural = verbose_name
