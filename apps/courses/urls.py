# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import ProfileCourseView,CreateCourseView,CourseDetailView,CourseModifyView,ResourceUploadView,CourseProjectView,CourseCommentView,CourseDownloadView,ResourceDeleteView,CreateHomeworkView,DeleteHomeworkView,CourseHomeworkView,UploadStudentHomeworkView,DeleteStudentHomeworkView

urlpatterns = [
    url(r'^mycourse/$', ProfileCourseView.as_view(), name="mycourse"),
    url(r'^create/$', CreateCourseView.as_view(), name="create"),
    url(r'^detail/$', CourseDetailView.as_view(), name="detail"),
    url(r'^project/$', CourseProjectView.as_view(), name="project"),
    url(r'^comment/$', CourseCommentView.as_view(), name="comment"),
    url(r'^download/$', CourseDownloadView.as_view(), name="download"),
    url(r'^course_update/$', CourseModifyView.as_view(), name="course_update"),
    url(r'^resource_upload/$', ResourceUploadView.as_view(), name="resource_upload"),
    url(r'^resource_delete/$', ResourceDeleteView.as_view(), name="resource_delete"),
    url(r'^homework_create/$', CreateHomeworkView.as_view(), name="homework_create"),
    url(r'^homework_delete/$', DeleteHomeworkView.as_view(), name="homework_delete"),
    url(r'^homework_detail/$', CourseHomeworkView.as_view(), name="homework_detail"),
    url(r'^student_hw_upload/$', UploadStudentHomeworkView.as_view(), name="student_hw_upload"),
    url(r'^student_hw_delete/$', DeleteStudentHomeworkView.as_view(), name="student_hw_delete"),
]