# _*_ coding:utf-8 _*_
import os,json
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.conf import settings
# Create your views here.
from datetime import datetime, timedelta
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserCourse,CourseComments,CommentComment
from django.contrib.auth.models import User
from .models import Course,CourseResource,CourseHomework,StudentHomework
from .forms import CreateCourseForm,CreateImageForm,CreateFileForm,CreateHomeworkForm,CreateDownloadForm,CreateSHForm







###個人資料顯示個人課程
class ProfileCourseView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        if request.user.extraprofile.identify == 'teacher':
            all_course = Course.objects.all()
            f_course = all_course.filter(instructor = request.user.id)
            #對課程機構進行分頁
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            # Provide Paginator with the request object for complete querystring generation
            p = Paginator(f_course, 5, request=request)
            course_list = p.page(page)
            
            
        elif request.user.extraprofile.identify == 'student':
            my_course = UserCourse.objects.filter(user_id=request.user.id)
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            # Provide Paginator with the request object for complete querystring generation
            p = Paginator(my_course, 5, request=request)
            course_list = p.page(page)

        return render(request, 'profile_course.html', {
                'course_list':course_list,
        })
        



###建立課程
class CreateCourseView(View):
    
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        return render(request, 'profile_course.html')

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        createCourse_form = CreateCourseForm(request.POST)
        if createCourse_form.is_valid():
            course = Course()
            course_name = request.POST.get('newCourseName','')
            if Course.objects.filter(name=course_name):
                return HttpResponseRedirect('/courses/mycourse/')
            course.name = course_name
            course.desc = request.POST.get('newCourseDesc','')
            course.detail = request.POST.get('newCourseDetail','')
            course.instructor = request.user.id
            course.save()
            now_course = Course.objects.get(name=course_name)
            image_form = CreateImageForm(request.POST, request.FILES, instance=now_course)
            if image_form.is_valid():
                image_form.save()
        return HttpResponseRedirect('/courses/mycourse/')
        


        
###顯示課程資訊        
class CourseDetailView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        course_id = request.GET.get('id','')
        course = Course.objects.get(id=course_id)
        return render(request, 'course_detail.html', {'course':course, 'user':request.user})


###修改課程資訊
class CourseModifyView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        #修改課程詳細內容
        n_course = Course.objects.get(id=request.GET.get('id'))
        n_course.name = request.POST.get('courseName','')
        n_course.desc = request.POST.get('courseDesc','')
        n_course.detail = request.POST.get('courseDetail','')
        form_aux = CreateImageForm(request.POST, request.FILES)
        if form_aux.is_valid() and 'image' in request.FILES:
            if(n_course.image != 'img/course/default_course.jpg'):
                n_course.image.delete()
        image_form = CreateImageForm(request.POST, request.FILES, instance=n_course)
        if image_form.is_valid():
            image_form.save()
        n_course.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


###顯示作業列表        
class CourseProjectView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        course_id = request.GET.get('id','')
        course = Course.objects.get(id=course_id)
        all_homework = CourseHomework.objects.all()
        n_homework = all_homework.filter(course=course_id).order_by('limit_time')
        homework_num = n_homework.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(n_homework, 5, request=request)
        homework_list = p.page(page)
        return render(request, 'course_project.html', {'course':course, 'user':request.user, 'homework_list':homework_list, 'homework_num':homework_num})


###新增作業
class CreateHomeworkView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        createHomework_form = CreateHomeworkForm(request.POST)
        if createHomework_form.is_valid():
            course = Course.objects.get(id=request.GET.get('id',''))
            homework = CourseHomework()
            homework.course = course
            homework.name = request.POST.get('projectTitle')
            homework.desc = request.POST.get('projectDesc')
            homework.detail = request.POST.get('projectDetail')
            homework.limit_time = request.POST.get('projectLimitTime')
            homework.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

###刪除作業
class DeleteHomeworkView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        CourseHomework.objects.get(id=request.GET.get('h_id')).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


       
###顯示作業詳細資訊 id h_id
class CourseHomeworkView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        now_course = Course.objects.get(id=request.GET.get('id'))
        now_homework = CourseHomework.objects.get(id=request.GET.get('h_id'))
        now_studentHomework = StudentHomework.objects.all().filter(homework_id=request.GET.get('h_id'))
        my_hw = now_studentHomework.filter(user_id=request.user.id)
        HwIsSubmit = False
        if my_hw.exists():
            HwIsSubmit = True
        shHasSubmit = StudentHomework.objects.all().filter(homework_id=request.GET.get('h_id')).values_list('user_id', flat=True)
        theStudentInCourse = UserCourse.objects.all().filter(course_id=request.GET.get('id')).values_list('user_id', flat=True)
        shNotSubmitList = set(theStudentInCourse)-set(shHasSubmit)
        shNotSubmitList = list(shNotSubmitList)
        shNotSubmitList = [int(item) for item in shNotSubmitList]
        theStudentNotSubmit = []
        for person in shNotSubmitList:
                theStudentNotSubmit.append(User.objects.get(id=person).extraprofile.name)
        return render(request, 'course_project_detail.html', {'course':now_course, 'now_homework':now_homework, 'now_studentHomework':now_studentHomework, 'my_hw':my_hw, 'HwIsSubmit':HwIsSubmit, 'theStudentNotSubmit':theStudentNotSubmit})


###學生上傳作業 id h_id
class UploadStudentHomeworkView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        HwIsSubmit = False
        if StudentHomework.objects.all().filter(homework_id=request.GET.get('h_id'), user_id=request.user.id).exists():
            HwIsSubmit = True
        if HwIsSubmit == False and CourseHomework.objects.get(id=request.GET.get('h_id')).deadline_token == '0':
            new_sh = StudentHomework()
            new_sh.course = Course.objects.get(id=request.GET.get('id'))
            new_sh.homework = CourseHomework.objects.get(id=request.GET.get('h_id'))
            new_sh.user = request.user.extraprofile
            new_sh.save()
            now_sh = StudentHomework.objects.latest('id')
            sh_form = CreateSHForm(request.POST, request.FILES, instance=now_sh)
            if sh_form.is_valid():
                sh_form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


###刪除學生作業
class DeleteStudentHomeworkView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        now_sh =  StudentHomework.objects.get(user_id=request.user.id)
        now_sh.file.delete()
        now_sh.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





###討論區列表 id
class CourseCommentView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        course_id = request.GET.get('id','')
        course = Course.objects.get(id=course_id)
        all_comment = CourseComments.objects.all()
        all_reply = CommentComment.objects.all()
        n_comment = all_comment.filter(course = course_id).order_by('-add_time')
        commentHasReply = CourseComments.objects.annotate(num_reply=Count('commentcomment')).filter(num_reply__gt=0)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(n_comment, 5, request=request)
        comment_list = p.page(page)
        return render(request, 'course_comment.html', {'course':course, 'user':request.user, 'comment_list':comment_list, 'reply_list':all_reply, 'commentHasReply':commentHasReply})



###顯示下載列表 id
class CourseDownloadView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        course_id = request.GET.get('id','')
        course = Course.objects.get(id=course_id)
        all_file = CourseResource.objects.all()
        n_all_file = all_file.filter(course_id = course_id)
        file_num = n_all_file.count()
        #檔案項目進行分頁
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(n_all_file, 5, request=request)
        file_list = p.page(page)
        return render(request, 'course_download.html', {'course':course, 'user':request.user, 'file_list':file_list, 'file_num':file_num})



###上傳課件 id
class ResourceUploadView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        createDownload_form = CreateDownloadForm(request.POST)
        if createDownload_form.is_valid():
            course_source = CourseResource()
            course_source.course_id = request.GET.get('id')
            course_source.name = request.POST.get('newFileName')
            course_source.detail = request.POST.get('newFileDesc')
            course_source.save()
            now_course_source = CourseResource.objects.get(id=course_source.id)
            image_form = CreateFileForm(request.POST, request.FILES, instance=now_course_source)
            if image_form.is_valid():
                image_form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        

###刪除課件 resource_id
class ResourceDeleteView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/users/login/')
        resource_id = request.GET.get('resource_id')
        now_resource = CourseResource.objects.get(id=resource_id)
        now_resource.download.delete()
        now_resource.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
