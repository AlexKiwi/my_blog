import django_filters
from .models import Article, Comments


class ArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """

    class Meta:
        model = Article
        fields = ['category', 'tag', 'status']


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """
    class Meta:
        model = Comments
        fields = ['article']