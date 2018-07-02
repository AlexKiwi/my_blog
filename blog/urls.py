from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'com_list', CommentListViewSet, base_name='com-list')
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'suggests', SuggestViewSet)
router.register(r'tags', TagViewSet)
# TODO 匹配和顺序有关这个需要放在最后
router.register(r'', ArticleViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
]
