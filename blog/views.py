from __future__ import unicode_literals
import json
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
import error_code
from rest_framework import exceptions, mixins, viewsets, status
from .serializers import *
from .models import Category, Article, Tag, Comments
from rest_framework.views import APIView, exception_handler


class BlogAPIView(APIView):
    def get_exception_handler(self):
        return api_exception_handler


class FormatSuccessResponse(BlogAPIView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(FormatSuccessResponse, self).finalize_response(request, response, *args, **kwargs)

        if hasattr(response, 'render') and callable(response.render):
            response.render()

        if response.status_code >= 200 and response.status_code < 300:
            if response['Content-Type'].lower() == 'application/json':
                response.content = json.dumps({"return_code" : 0, "return_msg" : '成功', "data" : json.loads(response.content)})
            else:
                if str(response.content).lower == "success":
                    response.content = json.dumps({"return_code" : 0, "return_msg" : '成功', "data" : response.content})
                else:
                    response.content = json.dumps({"return_code" : 0, "return_msg" : '成功'})
                response['Content-Type'] = 'application/json'
        # TODO
        if response.status_code == 401:
            content = json.loads(response.content)
            if content['return_msg'] == "Signature has expired.":
                response.content = json.dumps({"return_code": 10006, "return_msg": '签名过期'})
            elif content['return_msg'] == "身份认证信息未提供。" or content['return_msg'] == 'Error decoding signature.':
                response.content = json.dumps({"return_code": 10005, "return_msg": '用户未登录'})
            else:
                response.content = json.dumps({"return_code": 10007, "return_msg": '未知登录错误'})
            # elif response.content['return_msg'] == "身份认证信息未提供。":
        if response.status_code == 403:
            content = json.loads(response.content)
            if content['return_msg'] == "您没有执行该操作的权限。":
                response.content = json.dumps({"return_code": 10009, "return_msg": '没有执行该操作的权限'})
        return response

    def encode_error(self, error_no):
        if hasattr(error_code, error_no):
            return {
                'return_code' : getattr(error_code, error_no),
                'return_msg' : getattr(error_code.ZhError, error_no)
            }
        else:
            return {
                'return_code' : getattr(error_code, 'SYSTEM_ERROR'),
                'return_msg' : error_no
            }


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    request = context['request']

    # Now add the HTTP status code to the response.
    if response is not None:
        # print response.data
        # if isinstance(exc, exceptions.ValidationError):
        print(response.data)
        data = response.data
        response.data = {}
        if 'detail' in data and not isinstance(data['detail'], (list, dict)):
            if hasattr(error_code, data['detail']):
                response.data['return_code'] = getattr(error_code, data['detail'])
                response.data['return_msg'] = getattr(error_code.ZhError, data['detail'])
            else:
                response.data['return_code'] = getattr(error_code, 'SYSTEM_ERROR')
                response.data['return_msg'] = data['detail']
        else:
            # data = {'detail': exc.detail}
            if isinstance(exc, exceptions.ValidationError):
                response.data['return_code'] = getattr(error_code, 'ERROR_CHECK_PARAM')
                response.data['return_msg'] = getattr(error_code.ZhError, 'ERROR_CHECK_PARAM')
                response.data['data'] = data
            else:
                response.data['return_code'] = getattr(error_code, 'UNDIFINED_ERROR')
                response.data['return_msg'] = getattr(error_code.ZhError, 'UNDIFINED_ERROR')
                response.data['data'] = data
    return response


# TODO 排序
# TODO 把格式化输入写到中间件或者上层
class CategoryViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.filter(is_delete=False)
    serializer_class = CategorySerializer


class CategoryDeleteView(FormatSuccessResponse, APIView):
    def patch(self, request, category_id):
        serializer = CategoryCheckSerializer(data={'category_id': category_id})
        serializer.is_valid(raise_exception=True)
        try:
            category = Category.objects.get(is_delete=False, pk=category_id)
        except Category.DoesNotExist:
            raise NotFound({'detail': 'ERROR_FIND_MODULE'})
        category.is_delete = True
        category.save()
        return Response('success', status=status.HTTP_200_OK)


class ArticleViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.filter(is_delete=False)
    serializer_class = ArticleSerializer


class ArticleDeleteView(FormatSuccessResponse, APIView):
    def patch(self, request, article_id):
        serializer = ArticleCheckSerializer(data={'category_id': article_id})
        serializer.is_valid(raise_exception=True)
        try:
            article = Article.objects.get(is_delete=False, pk=article_id)
        except Article.DoesNotExist:
            raise NotFound({'detail': 'ERROR_FIND_MODULE'})
        article.is_delete = True
        article.save()
        return Response('success', status=status.HTTP_200_OK)


class TagViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.filter(is_delete=False)
    serializer_class = TagSerializer


class TagDeleteView(FormatSuccessResponse, APIView):
    def patch(self, request, tag_id):
        serializer = TagCheckSerializer(data={'tag_id': tag_id})
        serializer.is_valid(raise_exception=True)
        try:
            tag = Article.objects.get(is_delete=False, pk=tag_id)
        except Tag.DoesNotExist:
            raise NotFound({'detail': 'ERROR_FIND_MODULE'})
        tag.is_delete = True
        tag.save()
        return Response('success', status=status.HTTP_200_OK)


class CommentViewSet(FormatSuccessResponse, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Comments.objects.filter(is_delete=False)
    serializer_class = CommentsSerializer


class CommentDeleteView(FormatSuccessResponse, APIView):
    def patch(self, request, comment_id):
        serializer = CommentsCheckSerializer(data={'comment_id': comment_id})
        serializer.is_valid(raise_exception=True)
        try:
            comment = Comments.objects.get(is_delete=False, pk=comment_id)
        except Comments.DoesNotExist:
            raise NotFound({'detail': 'ERROR_FIND_MODULE'})
        comment.is_delete = True
        comment.save()
        return Response('success', status=status.HTTP_200_OK)


