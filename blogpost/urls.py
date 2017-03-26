"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import BlogList, PostList, PostView, AddBlogView, AddPostView, UpdateBlogView, UpdatePostView
from django.conf import settings

urlpatterns = [
    url(r'^blogs/$', BlogList.as_view(), name="blogs"),
    url(r'^blogs/id(?P<blog_id>\d+)$', PostList.as_view(), name="blogid"),
    url(r'^posts/id(?P<pk>\d+)$', PostView.as_view(), name="postid"),
    url(r'^blogs/create/$', AddBlogView.as_view(), name="addblog"),
    url(r'^posts/create/$', AddPostView.as_view(), name="addpost"),
    url(r'^blogs/id(?P<pk>\d+)/edit/$', UpdateBlogView.as_view(), name="editblog"),
    url(r'^posts/id(?P<pk>\d+)/edit/$', UpdatePostView.as_view(), name="editpost"),
]


if settings.DEBUG is True:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
