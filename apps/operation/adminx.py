# _*_ coding: utf-8 _*_

import xadmin

from .models import UserAsk,UserCourse,UserMessage,CourseComments,CommentComment


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    

class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    

class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comment', 'like', 'location', 'picture', 'sound', 'video', 'add_time']
    search_fields = ['user', 'course', 'comment', 'like', 'location', 'picture', 'sound', 'video']
    list_filter = ['user', 'course', 'comment', 'like', 'location', 'picture', 'sound', 'video', 'add_time']

class CommentCommentAdmin(object):
    list_display = ['user', 'title', 'comment', 'like', 'add_time']
    search_fields = ['user', 'title', 'comment', 'like']
    list_filter = ['user', 'title', 'comment', 'like', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(CommentComment, CommentCommentAdmin)
