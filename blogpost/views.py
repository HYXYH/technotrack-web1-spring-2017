# coding: utf-8
from django.conf import settings
from django import forms

from comments.views import CommentForm
from django.shortcuts import get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Blog, Post, Like
from django.http import HttpResponse, JsonResponse
from django.db import models


class AddPostView(CreateView):
    template_name = "blogpost/edit.html"
    model = Post
    fields = ('blog', 'title', 'image', 'description_title', 'text', 'is_draft')
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
        # context['form'].fields['blog'].queryset = Blog.objects.filter(author=self.request.user)
        context['edit_mode_message'] = 'Create post'
        context['data_id'] = 'post-block-{}'
        context['data_url'] = resolve_url('blogpost:addpost')
        return context


class UpdatePostView(UpdateView):
    template_name = "blogpost/edit.html"
    model = Post
    fields = ('title', 'image', 'description_title', 'text', 'is_draft')
    blog_id = None

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):

        return resolve_url('blogpost:blogid', self.blog_id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.blog_id = form.instance.blog.id
        return super(UpdatePostView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Edit post'
        context['data_id'] = 'post-block-{}'.format(self.object.id)
        context['data_url'] = resolve_url('blogpost:editpost', self.object.id)
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
        context['data_id'] = 'blog-{}'
        context['data_url'] = resolve_url('blogpost:addblog')
        return context


class UpdateBlogView(UpdateView):
    template_name = "blogpost/edit.html"
    model = Blog
    fields = ('title', 'categories', 'image', 'text')

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def get_success_url(self):
        return resolve_url('blogpost:blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdateBlogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateBlogView, self).get_context_data(**kwargs)
        context['edit_mode_message'] = 'Edit blog'
        context['data_id'] = 'blog-{}'.format(self.object.id)
        context['data_url'] = resolve_url('blogpost:editblog', self.object.id)
        return context


class SortForm(forms.Form):

    sort = forms.ChoiceField(choices=(
        ('title', 'Заголовок'),
        ('author', 'Автор'),
        ('-created_at', 'Время'),
        ('text', 'Описание'),
        ('-rate', 'Рейтинг'),
        ('-comment_count', 'Обсуждаемые')
    ))
    search = forms.CharField(required=False)


# comments: show errors

class BlogList(ListView):
    template_name = "blogpost/blogs.html"
    sort_form = None

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.sort_form = SortForm(self.request.GET)
        return super(BlogList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['sort_form'] = self.sort_form
        return context

    def get_queryset(self):
        qs = Blog.objects.all()
        qs = qs.annotate_everything()

        if self.sort_form.is_valid():
            #fixme: не срабатывает, хотя выполняется
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
        qs = Post.objects.filter(blog=self.blog)
        # fixme: не работает при анонимном юзере
        qs = qs.posts_for_user(self.request.user)
        qs = qs.annotate_everything()
        qs = qs.get_likes()
        return qs

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['sort_form'] = SortForm() # just for good look
        context['comment_form'] = CommentForm()
        return context


# default='default_images/no_post_image.jpg'


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "blogpost/postdetails.html"
    queryset = Post.objects.annotate_everything()

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    # в object будет лежать Post.get(id=context['pk'])


class RatesView(View):

    def get(self, request):
        ids = request.GET.get('ids', '')
        ids = ids.split(',')
        rates = dict(Post.objects.filter(id__in=ids).values_list('id', 'rate'))
        return JsonResponse(rates)


class UpdateRateView(View):

    likedpost = None
    likes = None
    score = None

    def dispatch(self, request, pk=None, rate=None, *args, **kwargs):
        self.likedpost = get_object_or_404(Post.objects.all(), id=pk)
        self.likes = Like.objects.filter(author=request.user, post=self.likedpost)
        if rate == 'up':
            self.score = 1
        if rate == 'down':
            self.score = -1
        return super(UpdateRateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if len(self.likes) == 0:
            like = Like(author=request.user, post=self.likedpost, score=self.score)
            like.save()
            self.likedpost.rate += self.score
            self.likedpost.save()
        else:
            like = self.likes.first()
            like.score += self.score
            if like.score > 1 or like.score < -1:
                return HttpResponse("Cheating is bad")
            else:
                like.save()
                self.likedpost.rate += self.score
                self.likedpost.save()

        return HttpResponse(self.likedpost.rate)
