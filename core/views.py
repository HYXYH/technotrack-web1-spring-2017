from django.shortcuts import render
from django.views.generic.base import TemplateView
from blogpost.models import Blog, Post
from core.models import User
# Create your views here.


class LoginView(TemplateView):
    template_name = "core/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['blogs_count'] = Blog.objects.all().count()
        context['posts_count'] = Post.objects.all().count()
        context['user_count'] = User.objects.all().count()
        return context
