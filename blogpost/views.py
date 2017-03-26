# coding: utf-8
from django.conf import settings
from django.urls import reverse
from comments.views import CommentForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Blog, Post


class AddPostView(CreateView):
    template_name = "blogpost/edit_post.html"
    model = Post
    fields = ('blog', 'title', 'image', 'description_title', 'text')
    # success_url = reverse('blogpost:blogs')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.rate = 0
        self.success_url = '/blogs/id{}'.format(form.instance.blog.id)
        return super(AddPostView, self).form_valid(form)


class UpdatePostView(UpdateView):
    template_name = "blogpost/edit_post.html"
    model = Post
    fields = ('title', 'image', 'description_title', 'text')
    # success_url = reverse('blogpost:blogs')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.rate = 0
        self.success_url = '/blogs/id{}'.format(form.instance.blog.id)
        return super(UpdatePostView, self).form_valid(form)


class AddBlogView(CreateView):
    template_name = "blogpost/edit_blog.html"
    model = Blog
    fields = ('name', 'categories', 'image', 'description_title', 'text')
    # success_url = reverse('blogpost:blogs')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddBlogView, self).form_valid(form)


class UpdateBlogView(UpdateView):
    template_name = "blogpost/edit_blog.html"
    model = Blog
    fields = ('name', 'categories', 'image', 'description_title', 'text')
    # success_url = reverse('blogpost:blogs')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateBlogView, self).form_valid(form)


class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = "blogpost/blogs.html"

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['default_post_image'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_post_image.jpg')
        context['default_avatar'] = "{}{}".format(settings.MEDIA_URL, 'default_images/no_avatar.png')
        return context


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
