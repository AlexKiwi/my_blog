"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from blog import views as blog_views
from user import views as user_views


router = routers.DefaultRouter()

router.register(r'categories', blog_views.CategoryViewSet)
router.register(r'articles', blog_views.ArticleViewSet)
router.register(r'tags', blog_views.TagViewSet)
router.register(r'comments', blog_views.CommentViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^admin-api/login/', LoginView.as_view()),
    url(r'docs/', include_docs_urls(title="乐荐代后台管理系统")),
    url(r'^category_delete/(?P<category_id>\d+)$', blog_views.CategoryDeleteView.as_view()),
    url(r'^article_delete/(?P<article_id>\d+)$', blog_views.ArticleDeleteView.as_view()),
    url(r'^tag_delete/(?P<tag_id>\d+)$', blog_views.TagDeleteView.as_view()),
    url(r'^comments_delete/(?P<comment_id>\d+)$', blog_views.CommentDeleteView.as_view()),
]
