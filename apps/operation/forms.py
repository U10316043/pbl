# _*_ coding:utf-8 _*_
from django import forms


class CreateReplyForm(forms.Form):
    replyDetail = forms.CharField(required=True)
    