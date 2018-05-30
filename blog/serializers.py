from rest_framework import serializers

from .models import Category, Article, Tag, Comments, Suggest


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('__all__')


class SuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggest
        fields = ('__all__')


class CategoryCheckSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True)


class ArticleCheckSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True)


class TagCheckSerializer(serializers.Serializer):
    tag_id = serializers.IntegerField(required=True)


class CommentsCheckSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=True)


class SuggestCheckSerializer(serializers.Serializer):
    suggest_id = serializers.IntegerField(required=True)
