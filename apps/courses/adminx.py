# _*_ coding: utf-8 _*_

import xadmin
from xadmin import views
from .models import Course,CourseResource,CourseHomework,StudentHomework

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'instructor', 'image', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'instructor', 'image']
    list_filter = ['name', 'desc', 'detail', 'instructor', 'image', 'add_time']
    
class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']
    
class CourseHomeworkAdmin(object):
    list_display = ['course', 'name', 'desc', 'detail', 'uploadFile', 'deadline_token', 'limit_time', 'add_time']
    search_fields = ['course', 'name', 'desc', 'detail', 'uploadFile', 'deadline_token', 'limit_time']
    list_filter = ['course', 'name', 'desc', 'detail', 'uploadFile', 'deadline_token', 'limit_time', 'add_time']
    
class StudentHomeworkAdmin(object):
    list_display = ['course', 'homework', 'user', 'file', 'add_time']
    search_fields = ['course', 'homework', 'user', 'file']
    list_filter = ['course', 'homework', 'user', 'file', 'add_time']
    
    
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(CourseHomework,CourseHomeworkAdmin)
xadmin.site.register(StudentHomework,StudentHomeworkAdmin)
