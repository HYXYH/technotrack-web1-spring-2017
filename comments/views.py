from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from blogpost.models import Post
from models import Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView


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


def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(author=request.user, text=form.cleaned_data['text'], post=form.cleaned_data['post'])
            comment.save()
            return redirect('{}#comments{}'.format(request.META.get('HTTP_REFERER'), comment.post.id))
