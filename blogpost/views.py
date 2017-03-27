# coding: utf-8
from django.conf import settings
from django import forms

from comments.views import CommentForm
from django.shortcuts import get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Blog, Post


class AddPostView(CreateView):
    template_name = "blogpost/edit.html"
    model = Post
    fields = ('blog', 'title', 'image', 'description_title', 'text')
    blog_id = None

    def get_success_url(self):
        return resolve_url('blogpost:blogid', self.blog_id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.rate = 0
        self.blog_id = form.instance.blog.id
        return super(AddPostView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPostView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Create post'
        return context


class UpdatePostView(UpdateView):
    template_name = "blogpost/edit.html"
    model = Post
    fields = ('title', 'image', 'description_title', 'text')
    blog_id = None

    def get_success_url(self):
        return resolve_url('blogpost:blogid', self.blog_id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.blog_id = form.instance.blog.id
        return super(UpdatePostView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Edit post'
        return context


class AddBlogView(CreateView):
    template_name = "blogpost/edit.html"
    model = Blog
    fields = ('title', 'categories', 'image', 'text')

    def get_success_url(self):
        return resolve_url('blogpost:blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddBlogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddBlogView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Create blog'
        return context


class UpdateBlogView(UpdateView):
    template_name = "blogpost/edit.html"
    model = Blog
    fields = ('title', 'categories', 'image', 'text')

    def get_success_url(self):
        return resolve_url('blogpost:blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        print super(UpdateBlogView, self).form_valid(form)
        return super(UpdateBlogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateBlogView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Edit blog'
        return context


class SortForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('title', 'Title'),
        ('author', 'Author'),
        ('created_at', 'Time'),
        ('text', 'Description')
    ))
    search = forms.CharField(required=False)


class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = "blogpost/blogs.html"
    sort_form = None

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.sort_form = SortForm(self.request.GET)
        return super(BlogList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['sort_form'] = self.sort_form
        context['default_post_image'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_post_image.jpg')
        context['default_avatar'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_avatar.png')
        return context

    def get_queryset(self):
        qs = super(BlogList, self).get_queryset()
        if self.sort_form.is_valid():
            qs = qs.order_by(self.sort_form.cleaned_data['sort'])
            if self.sort_form.cleaned_data['search']:
                qs = qs.filter(title__icontains=self.sort_form.cleaned_data['search'])
        return qs


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
        context['comment_form'] = CommentForm()
        context['default_post_image'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_post_image.jpg')
        context['default_avatar'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_avatar.png')
        return context


# default='default_images/no_post_image.jpg'


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "blogpost/postdetails.html"

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['default_post_image'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_post_image.jpg')
        context['default_avatar'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_avatar.png')
        return context
    # в object будет лежать Post.get(id=context['pk'])
