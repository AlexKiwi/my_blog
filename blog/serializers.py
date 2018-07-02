import traceback

from rest_framework import serializers
from rest_framework.compat import set_many
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

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

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)
        try:
            if 'comment' in validated_data:
                if validated_data['comment'].comment_top:
                    instance = ModelClass.objects.create(**validated_data,
                                                         comment_top=validated_data['comment'].comment_top)
                else:
                    instance = ModelClass.objects.create(**validated_data, comment_top=validated_data['comment'])
            else:
                instance = ModelClass.objects.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.objects.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.objects.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass.__name__,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                set_many(instance, field_name, value)

        return instance


class CommentListSerializer(serializers.ModelSerializer):
    com_list = CommentsSerializer(many=True)

    class Meta:
        model = Comments
        fields = ('id', 'name', 'email', 'comment', 'article', 'comment_top', 'content', 'com_list', 'created_at',
                  'updated_at', 'deleted_at')


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
