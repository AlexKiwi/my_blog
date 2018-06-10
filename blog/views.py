from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import detail_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import mixins, viewsets, generics, status
from blog.base_view import FormatSuccessResponse, GenericForAdminViewSet, LogicalDeleteMixin
from .filters import ArticleFilter, CommentFilter
from .serializers import *
from .models import Category, Article, Tag, Comments, Suggest
from .permissions import IsAuthenticatedSuperUserOrReadOnly, IsAuthenticatedSuperUserOrCreateReadOnly, \
    IsAuthenticatedSuperUserOrCreateOnly, ArticlePermission


class CategoryViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Category.objects.filter(deleted_at=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedSuperUserOrReadOnly,)


# 可以自定义每页多少条数据
class StandardesultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


# TODO 搜索功能
class ArticleViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Article.objects.filter(deleted_at=None)
    serializer_class = ArticleSerializer
    permission_classes = (ArticlePermission,)
    pagination_class = StandardesultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter
    ordering_fields = '__all__'
    ordering = ('display_order',)

    # TODO 会不会出现不增加的情况 加锁？
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # TODO 加锁
    @detail_route(methods=['patch'], url_path='likes')
    def add_like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.likes += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['patch'], url_path='top')
    def topped(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.display_order = 1
        instance.save()
        article_list = Article.objects.exclude(pk=instance.id).filter(display_order=1)
        for article in article_list:
            article.display_order = 999
            article.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(FormatSuccessResponse, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Tag.objects.filter(deleted_at=None)
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedSuperUserOrReadOnly,)


# TODO 别人评论会发邮件同时 自己回复评论也要通知别人
class CommentViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericForAdminViewSet):
    queryset = Comments.objects.filter(deleted_at=None)
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedSuperUserOrCreateReadOnly,)

    @detail_route(methods=['patch'], url_path='delete')
    def delete_obj(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.logical_delete()
        obj_list = Comments.objects.filter(comment_top=obj)
        for obj in obj_list:
            obj.logical_delete()
        return Response('success', status=status.HTTP_200_OK)


class CommentListViewSet(FormatSuccessResponse, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentListSerializer
    pagination_class = StandardesultsSetPagination

    def get_queryset(self):
        comment_list = Comments.objects.filter(comment=None, comment_top=None, deleted_at=None)
        for comment in comment_list:
            comment.com_list = comment.top_comments.filter(deleted_at=None)
            comment.save()
        return comment_list


# TODO 提出建议发邮件通知 同时发邮件感谢别人
class SuggestViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Suggest.objects.filter(deleted_at=None)
    serializer_class = SuggestSerializer
    pagination_class = StandardesultsSetPagination
    permission_classes = (IsAuthenticatedSuperUserOrCreateOnly,)

