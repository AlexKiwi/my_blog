import re

from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS


# 标签，分类，文章的创建修改删除只有超级管理员才有权限，读权限所有人都有
# 评论，建议所有人都有创建和读的权限 但是修改和删除只有超级管理员有
# 编写文章的时候可以 登录之后加入投稿 或者个人中心


class IsSuperUser(BasePermission):
    """
    超级用户权限
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAuthenticatedSuperUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a superuser, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS or (request.user and is_authenticated(request.user) and
                                                   request.user.is_superuser)
        )


class IsAuthenticatedSuperUserOrCreateReadOnly(BasePermission):
    """
    The request is a authenticated as a superuser, or is a read-create-only request
    """

    def has_permission(self, request, view):
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS', 'POST') or
            (request.user and is_authenticated(request.user) and request.user.is_superuser)
        )


class IsAuthenticatedSuperUserOrCreateOnly(BasePermission):
    """
    The request is a authenticated as a superuser, or is a read-create-only request
    """

    def has_permission(self, request, view):
        return (
            request.method in ('HEAD', 'OPTIONS', 'POST') or
            (request.user and is_authenticated(request.user) and request.user.is_superuser)
        )


class ArticlePermission(BasePermission):
    def has_permission(self, request, view):
        likes = re.compile(r'^/blog/\d+/likes/$')
        print(request.path)
        return (
            (request.method in SAFE_METHODS or likes.match(request.path)) or
            (request.user and is_authenticated(request.user) and request.user.is_superuser))
