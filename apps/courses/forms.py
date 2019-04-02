# _*_ coding:utf-8 _*_
from django import forms
from .models import Course,CourseResource,StudentHomework


class CreateCourseForm(forms.Form):
    newCourseName = forms.CharField(required=True, min_length=2)
    newCourseDesc = forms.CharField(required=True)
    newCourseDetail = forms.CharField(required=True)
    

class CreateHomeworkForm(forms.Form):
    projectTitle = forms.CharField(required=True)
    
    
class CreateDownloadForm(forms.Form):
    newFileName = forms.CharField(required=True)

    
class CreateImageForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image']
        
class CreateFileForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['download']
        
class CreateSHForm(forms.ModelForm):
    class Meta:
        model = StudentHomework
        fields = ['file']