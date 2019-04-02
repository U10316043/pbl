# _*_ encoding:utf-8 _*_
from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.contrib import messages

from .models import ExtraProfile
from .forms import LoginForm,RegisterForm,UploadImageForm



# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {'user':user})
                else:
                    return render(request, 'login.html', {'msg':'用戶尚未啟用'})
            else:
                return render(request, 'login.html', {'msg':'帳號或密碼錯誤'})
        else:
            return render(request, 'login.html', {'login_form':login_form})
            
            
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html')


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
            user_profile.is_active = False
            user_profile.save()
            return render(request, 'login.html', {'success':'註冊成功，請登入'})
        else:
            return render(request, 'register.html', {'register_form':register_form})
            
            
class ProfileHomeView(View):
    def get(self, request):
        return render(request, 'profile_home.html')


class UpdateProfileView(View):
    def get(self, request):
        return render(request, 'profile_home.html')
    def post(self, request):
        last_name = request.POST.get("lastname","")
        first_name = request.POST.get("firstname","")
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        gender = request.POST.get("gender","")
        now_user = request.user
        now_user.first_name = first_name
        now_user.last_name = last_name
        now_user.email = email
        now_user.extraprofile.name = name
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
        messages.success(request, '修改成功!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
class ProfileHelpView(View):
    def get(self, request):
        return render(request, 'profile_help.html')
