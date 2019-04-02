# _*_ encoding:utf-8 _*_
import json

from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import RequestContext

from .models import ExtraProfile
from courses.models import CourseHomework
from operation.models import UserCourse
from .forms import LoginForm,RegisterForm,UploadImageForm



#首頁通知
class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            myCourse = UserCourse.objects.filter(user_id = request.user.id)
            myHomework = []
            for ChosenCourse in myCourse:
                for allMyHomework in CourseHomework.objects.filter(course_id=ChosenCourse.course):
                    myHomework.append(allMyHomework)
            myHomework.sort(key=lambda x: x.limit_time)
            return render(request, 'index.html', {'myHomework':myHomework,})
        return render(request, 'index.html')



#登入介面
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        response_data = {}
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response_data['status'] = 'logged'
                    response_data['name'] = user.extraprofile.name
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    response_data['status'] = 'alert'
                    response_data['message'] = '用戶尚未啟用'
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            else:
                response_data['status'] = 'alert'
                response_data['message'] = '帳號或密碼錯誤'
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
        else:
            response_data['status'] = 'alert'
            response_data['message'] = '格式錯誤'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
            
#登出介面
class LogoutView(View):
    def get(self, request):
        logout(request)
        response_data = {}
        response_data['status'] = 'logout'
        response_data['message'] = '登出成功'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

#註冊頁面
class RegisterView(View):
    
    def get(self, request):
        
        register_form = RegisterForm()
        
        return render(request, 'register.html', {'register_form':register_form})
        
    def post(self, request):
        
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            user_name = request.POST.get("username","")
            
            if User.objects.filter(username=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'用戶已經存在'})
            
            pass_word = request.POST.get("password","")
	    user_profile = User()
            user_profile.username = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = True
            user_profile.save()
            ExtraProfile.objects.create(user_id=User.objects.latest('id').id)
	    EP = ExtraProfile.objects.latest('user_id')
	    EP.name = user_name
	    EP.identify = 'student'
	    EP.save()

            return render(request, 'login.html', {'success':'註冊成功，請登入'})
        else:
            return render(request, 'register.html', {'register_form':register_form})
            


#使用者個人資料頁面            
class ProfileHomeView(View):
    def get(self, request):
        return render(request, 'profile_home.html')


#更新個人資料
class UpdateProfileView(View):
    def get(self, request):
        return render(request, 'profile_home.html')
    def post(self, request):
        last_name = request.POST.get("lastname","")
        first_name = request.POST.get("firstname","")
        email = request.POST.get("email","")
	name = request.POST.get("stdNum","")
        gender = request.POST.get("gender","")
        now_user = request.user
	now_user = name
        now_user.first_name = first_name
        now_user.last_name = last_name
        now_user.email = email
        now_user.extraprofile.gender = gender
        
        #刪除舊圖
        form_aux = UploadImageForm(request.POST, request.FILES)
        if form_aux.is_valid() and 'image' in request.FILES:
            if(now_user.extraprofile.image != 'img/user/default_user.png'):
                now_user.extraprofile.image.delete()
        #存入新圖
        image_form = UploadImageForm(request.POST, request.FILES, instance=now_user.extraprofile)
        if image_form.is_valid():
            image_form.save()
        
        now_user.save()
        now_user.extraprofile.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

       
class ProfileHelpView(View):
    def get(self, request):
        return render(request, 'profile_help.html')
