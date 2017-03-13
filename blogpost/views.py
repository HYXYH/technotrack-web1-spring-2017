# coding: utf-8
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Blog, Post


class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = "blogpost/blogs.html"


class PostList(ListView):
    def get_queryset(self):
        return Post.objects.filter(blog=self.kwargs['blog_id'])

    template_name = "blogpost/posts.html"


class PostView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        return context

    model = Post
    template_name = "blogpost/postdetails.html"
    # Можно ли передать Post.objects.get(id=context['post_id']) попроще? как вытащить post_id?
