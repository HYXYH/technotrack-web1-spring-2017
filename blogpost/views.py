# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog, Post


class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = "blogpost/blogs.html"


class PostList2(ListView):
    def get_queryset(self):
        return Post.objects.filter(blog=self.kwargs['blog_id'])

    template_name = "blogpost/posts.html"


class PostList(ListView):
    blog = None
    template_name = "blogpost/posts.html"

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), id=blog_id)
        return super(PostList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(blog=self.blog)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        return context


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "blogpost/postdetails.html"
    # в object будет лежать Post.get(id=context['pk'])
