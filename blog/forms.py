# coding=utf-8

# """
# 模块描述：
#
# 作者：qzcxh
#
# “”“
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('username','email','body')