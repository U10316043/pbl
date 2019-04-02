# _*_ coding:utf-8 _*_
import json,os,time,math
import numpy as np
import scipy.io.wavfile
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
# Create your views here.
from .forms import CreateReplyForm
from .models import CourseComments,CommentComment,CommentPostLike,ReplyPostLike
from courses.models import Course


location = None



###取得位置
class getLocation(View):
    def post(self,request):
        response_data = {}
        response_data['message'] = 'success get location!'
        global location
        location = request.POST.get('commentlocation')
        print(location)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


###刪除留言
class DeleteCommentsView(View):
    def get(self,request):
        comment_id = request.GET.get('comment_id')
        now_comment = CourseComments.objects.get(id=comment_id)
        if now_comment.picture:
            os.remove(settings.MEDIA_ROOT+'/'+now_comment.picture)
        if now_comment.sound:
            os.remove(settings.MEDIA_ROOT+'/'+now_comment.sound)
	if now_comment.video:
	    os.remove(settings.MEDIA_ROOT+'/'+now_comment.video)
        now_comment.delete()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






###新增留言
class CourseCommentsView(View):
    def post(self, request):
        response_data = {}
        if(request.POST.get('commentDetail') == ''):
            response_data['message'] = '不可為空!'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            cc = CourseComments()
            cc.user = request.user.extraprofile
            cc.course = Course.objects.get(id=request.GET.get('id'))
            cc.comment = request.POST.get('commentDetail')
            cc.location = location
            if(request.FILES.get('picture', False)):
                pictureName =  time.strftime("%Y%m%d-%H%M%S")+".jpg"
                if not os.path.exists('media/course/comment/'+request.GET.get('id')):
                    os.makedirs('media/course/comment/'+request.GET.get('id'))
                uploadedFile = open("media/course/comment/"+request.GET.get('id')+"/"+pictureName, "wb")
                uploadedFile.write(request.FILES['picture'].read())
                uploadedFile.close()
                cc.picture = 'course/comment/'+request.GET.get('id')+"/"+pictureName
            if(request.FILES.get('blob', False)):
                soundName = time.strftime("%Y%m%d-%H%M%S")+".mp3"
                if not os.path.exists('media/sound/course_id_'+request.GET.get('id')):
                    os.makedirs('media/sound/course_id_'+request.GET.get('id'))
                uploadedFile = open("media/sound/course_id_"+request.GET.get('id')+"/"+soundName, "wb")
                uploadedFile.write(request.FILES['blob'].read())
                uploadedFile.close()
                cc.sound = 'sound/course_id_'+request.GET.get('id')+"/"+soundName
	    if(request.FILES.get('video', False)):
                videoName =  time.strftime("%Y%m%d-%H%M%S")+".mp4"
                if not os.path.exists('media/course/comment/'+request.GET.get('id')):
                    os.makedirs('media/course/comment/'+request.GET.get('id'))
                uploadedFile = open("media/course/comment/"+request.GET.get('id')+"/"+videoName, "wb")
                uploadedFile.write(request.FILES['video'].read())
                uploadedFile.close()
                cc.video = 'course/comment/'+request.GET.get('id')+"/"+videoName
            cc.save()
            now_comment = CourseComments.objects.latest('id')
            print(now_comment.comment)
            
            response_data['message'] = 'create comment success'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        
###新增回覆
class ReplyCommentsView(View):
    def post(self, request):
        createReply_form = CreateReplyForm(request.POST)
        if createReply_form.is_valid():
            rc = CommentComment()
            rc.user = request.user.extraprofile
            rc.title = CourseComments.objects.get(id=request.GET.get('comment_id'))
            rc.comment = request.POST.get('replyDetail')
            rc.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

###送出讚
class CommentPostLikeSubmit(View):
    def post(self,request):
        response_data = {}
        cpl = CommentPostLike();
        cpl.title =  CourseComments.objects.get(id=request.POST.get('comment_id'))
        cpl.user = request.user.extraprofile
        cpl.save()
        n_cpl = CommentPostLike.objects.all().filter(title_id = request.POST.get('comment_id')).count()
        cc = CourseComments.objects.get(id=request.POST.get('comment_id'))
        cc.like = n_cpl
        cc.save()
        response_data['cpl'] = n_cpl
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
        
class ReplyPostLikeSubmit(View):
    def post(self,request):
        response_data = {}
        rpl = ReplyPostLike();
        rpl.title =  CommentComment.objects.get(id=request.POST.get('reply_id'))
        rpl.user = request.user.extraprofile
        rpl.save()
        n_rpl = ReplyPostLike.objects.all().filter(title_id = request.POST.get('reply_id')).count()
        rc = CommentComment.objects.get(id=request.POST.get('reply_id'))
        rc.like = n_rpl
        rc.save()
        response_data['rpl'] = n_rpl
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
