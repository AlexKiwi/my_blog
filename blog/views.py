from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import mixins
from blog.base_view import FormatSuccessResponse, GenericForAdminViewSet, LogicalDeleteMixin
from .filters import ArticleFilter
from .serializers import *
from .models import Category, Article, Tag, Comments, Suggest


class CategoryViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Category.objects.filter(deleted_at=None)
    serializer_class = CategorySerializer


class ArticleViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Article.objects.filter(deleted_at=None)
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter
    ordering_fields = '__all__'
    ordering = ('display_order',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.virews += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TagViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Tag.objects.filter(deleted_at=None)
    serializer_class = TagSerializer


class CommentViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Comments.objects.filter(deleted_at=None)
    serializer_class = CommentsSerializer


class SuggestViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, LogicalDeleteMixin, GenericForAdminViewSet):
    queryset = Suggest.objects.filter()
