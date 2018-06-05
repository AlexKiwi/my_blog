import django_filters
from .models import Article


class ArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """

    class Meta:
        model = Article
        fields = ['category', 'tag', 'status']
