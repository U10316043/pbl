# _*_ coding:utf-8 _*_
from django.conf.urls import url
from .views import CourseCommentsView,ReplyCommentsView,getLocation,CommentPostLikeSubmit,ReplyPostLikeSubmit,DeleteCommentsView


urlpatterns = [
    url(r'^create_comment/$', CourseCommentsView.as_view(), name="create_comment"),
    url(r'^reply_comment/$', ReplyCommentsView.as_view(), name="reply_comment"),
    url(r'^delete_comment/$', DeleteCommentsView.as_view(), name="delete_comment"),
    url(r'^getLocation/$', getLocation.as_view(), name="getLocation"),
    url(r'^updateLike/$', CommentPostLikeSubmit.as_view(), name="updateLike"),
    url(r'^updateReplyLike/$', ReplyPostLikeSubmit.as_view(), name="updateReplyLike"),
]