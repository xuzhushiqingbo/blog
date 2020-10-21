import json

from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, generics, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LehuXuexi.settings import MEDIA_ROOT, MEDIA_URL, YU_MING
from .filters import ArticleFilter
from .models import Article, BlogCategory, BlogTag, ArticleImage
from .serializers import ArticleSimpleSerializer, BlogCategorySerializer, BlogTagSerializer, ArticleDetailSerializer, \
    ArticleCreateSerializer, ArticleImageSerializer


# class ArticleListView(APIView):
#     """
#     列出所有文章
#     """
#     def get(self, request, format=None):
#         articles = Article.objects.all()[:10]
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArticleListView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Article.objects.all()[:5]
#     serializer_class = ArticleSimpleSerializer
#     authentication_classes = (TokenAuthentication,)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StandardResultsSetPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LimitResultsSetPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    default_limit = 10
    max_limit = 1000



class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSimpleSerializer
    # authentication_classes = (TokenAuthentication, )
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]


class ArticleListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """文章列表页的分页搜索过滤排序"""
    queryset = Article.objects.all()
    # serializer_class = ArticleSimpleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    # filterset_fields = ['category', 'user', 'title', 'click_num']
    search_fields = ['title', 'brief', 'content']
    ordering_fields = ['click_num', 'favor_num', 'add_time', 'comment_num']

    def get_serializer_class(self):
        # return ArticleSimpleSerializer
        if self.action == 'list':
            return ArticleSimpleSerializer
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSimpleSerializer

    # def get_queryset(self):
    #     queryset = Article.objects.all()
    #     click_num = self.request.query_params.get('clck', 0)
    #     if click_num:
    #         queryset = queryset.filter(click_num__gte=30)
    #     return queryset


class BlogCategoryViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """文章列表页的分页搜索过滤排序"""
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogTagViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """博客标签列表"""
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    pagination_class = LimitResultsSetPagination


class ArticleCreateViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """创建文章"""
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class ArticleImageCreateViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """文章内部图片创建"""
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


class ArticleImageCreateView(APIView):

    def post(self, request, format=None):
        image = request.data['image']
        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
            save_path = MEDIA_ROOT + '/blogs/articles/content/' + image.name[-10:]
            # file_path服务器上保存图片的路径
            file_path = default_storage.save(save_path, image)
            # 把文件的URL返回给前端
            file_url = YU_MING + MEDIA_URL + 'blogs/articles/content/' + file_path.split('/')[-1]
            # print(MEDIA_URL)
            # print(file_url)
            return Response({'image': file_url}, status=status.HTTP_201_CREATED)
        else:
            message = '图像扩展名不正确！ 只接受：'+str(['jpg', 'jpeg', 'png', 'gif'])
            # return Response("xxx", status=status.HTTP_201_CREATED)
            return Response({'image': message}, status=status.HTTP_400_BAD_REQUEST)


