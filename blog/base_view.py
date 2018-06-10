import json
from django.http import Http404, JsonResponse
from django.shortcuts import _get_queryset
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView, exception_handler
from rest_framework.viewsets import ViewSetMixin
import error_code
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
# from rest_framework.schemas.generators import LinkNode, insert_into
from rest_framework.renderers import *
from rest_framework_swagger import renderers
from rest_framework.response import Response


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
        if response.status_code == 403:
            content = json.loads(response.content)
            if content['return_msg'] == "您没有执行该操作的权限。":
                response.content = json.dumps({"return_code": 10009, "return_msg": '没有执行该操作的权限'})
        return response

    def encode_error(self, error_no):
        if hasattr(error_code, error_no):
            return {
                'return_code': getattr(error_code, error_no),
                'return_msg': getattr(error_code.ZhError, error_no)
            }
        else:
            return {
                'return_code': getattr(error_code, 'SYSTEM_ERROR'),
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
        data = response.data
        response.data = {}
        if 'detail' in data and not isinstance(data['detail'], (list, dict)):
            # if isinstance(data['detail'], unicode):
            #     data['detail'] = data['detail'].encode('utf-8')
            print(type(data['detail']))
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


def get_object_or_not_found(klass, *args, **kwargs):
    """
    Uses get() to return an object, or raises a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    except queryset.model.DoesNotExist:
        # --------修改部分----------------
        # raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
        raise NotFound({'detail': 'ERROR_FIND_MODULE'})


# 重写了get_object() DoesNotExist会抛出自定义错误
class GenericAPIForAdminView(GenericAPIView):
    def get_object(self):
        """
                Returns the object the view is displaying.

                You may want to override this if you need to provide non-standard
                queryset lookups.  Eg if objects are referenced using multiple
                keyword arguments in the url conf.
                """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = get_object_or_not_found(queryset, **filter_kwargs)
        except (TypeError, ValueError):
            raise Http404

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class GenericForAdminViewSet(ViewSetMixin, GenericAPIForAdminView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class LogicalDeleteMixin(object):
    @detail_route(methods=['patch'], url_path='delete')
    def delete_obj(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.logical_delete()
        return Response('success', status=status.HTTP_200_OK)


# from rest_framework.schemas import SchemaGenerator
# class MySchemaGenerator(SchemaGenerator):
#
#     def get_links(self, request=None):
#         # from rest_framework.schemas.generators import LinkNode,
#         links = LinkNode()
#
#         paths = []
#         view_endpoints = []
#         for path, method, callback in self.endpoints:
#             view = self.create_view(callback, method, request)
#             path = self.coerce_path(path, method, view)
#             paths.append(path)
#             view_endpoints.append((path, method, view))
#
#         # Only generate the path prefix for paths that will be included
#         if not paths:
#             return None
#         prefix = self.determine_path_prefix(paths)
#
#         for path, method, view in view_endpoints:
#             if not self.has_view_permissions(path, method, view):
#                 continue
#             link = view.schema.get_link(path, method, base_url=self.url)
#             # 添加下面这一行方便在views编写过程中自定义参数.
#             link._fields += self.get_core_fields(view)
#
#             subpath = path[len(prefix):]
#             keys = self.get_keys(subpath, method, view)
#
#             # from rest_framework.schemas.generators import LinkNode, insert_into
#             insert_into(links, keys, link)
#
#         return links
#
#     # 从类中取出我们自定义的参数, 交给swagger 以生成接口文档.
#     def get_core_fields(self, view):
#         return getattr(view, 'coreapi_fields', ())


# class SwaggerSchemaView(APIView):
#     _ignore_model_permissions = True
#     exclude_from_schema = True
#
#     # from rest_framework.permissions import AllowAny
#     permission_classes = [AllowAny]
#     # from rest_framework_swagger import renderers
#     # from rest_framework.renderers import *
#     renderer_classes = [
#         CoreJSONRenderer,
#         renderers.OpenAPIRenderer,
#         renderers.SwaggerUIRenderer
#     ]
#
#     def get(self, request):
#         generator = MySchemaGenerator(title='xxxxx',
#                                       description='''xxxxx''')
#
#         schema = generator.get_schema(request=request)
#
#         # from rest_framework.response import Response
#         return Response(schema)
#
#
# def DocParam(name="default", location="query",
#              required=True, description=None, type="string",
#              *args, **kwargs):
#     return coreapi.Field(name=name, location=location,
#                          required=required, description=description,
#                          type=type)
#
#
# class ReturnJson(APIView):
#
#     coreapi_fields=(
#         DocParam("token"),
#     )
#
#     def get(self, request, *args, **kwargs):
#         return JsonResponse("Hello world!!!!!!!!++++++中文测试")

