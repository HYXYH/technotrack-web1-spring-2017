from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django import forms
from blogpost.models import Post
from models import Comment
from django.views.generic import View, DetailView
from django.http import JsonResponse


# Create your views here.


class CommentForm(forms.ModelForm):
    class Meta(object):
        model = Comment
        fields = ('text', 'post')

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['post'].widget = HiddenInput()
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['aria-describedby'] = 'sizing-addon3'
        self.fields['text'].widget.attrs['style'] = 'resize:none;'
        self.fields['text'].label = ''


class PostCommentsView(DetailView):

    model = Post
    template_name = "comments/comment_block_content.html"

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(author=request.user, text=form.cleaned_data['text'], post=form.cleaned_data['post'])
            comment.save()
        return super(PostCommentsView, self).get(self, request, *args, **kwargs)