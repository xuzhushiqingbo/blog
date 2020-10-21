"""LehuXuexi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


from LehuXuexi.settings import MEDIA_ROOT
from blogs import views as blog_views
from users import views as user_views


router = DefaultRouter()
# article_list = ArticleListViewset.as_view({'get': 'list', 'post': 'create'})
router.register(r'articles', blog_views.ArticleListViewset, basename='article_list_viewset')
router.register(r'article/create', blog_views.ArticleCreateViewset, basename='article_create_viewset')
router.register(r'article/images/create', blog_views.ArticleImageCreateViewset, basename='article_image_create_viewset')
router.register(r'categories', blog_views.BlogCategoryViewset, basename='categories_viewset')
router.register(r'tags', blog_views.BlogTagViewset, basename='tags_viewset')
router.register(r'verifycodes', user_views.VerifyCodeViewset, basename='verifycodes_viewset')
router.register(r'register', user_views.UserRegisterViewset, basename='register_viewset')
router.register(r'users', user_views.UserDetailViewset, basename='user_viewset')
# 所有V1板的API
api_V1_urls = router.urls + [
    path('articles0/', blog_views.ArticleListView.as_view(), name='article0-list'),
    #上传文章插图的url
    path('article/image/', blog_views.ArticleImageCreateView.as_view(), name='article_image'),
    path('user/avatar/', user_views.UserAvatarUpdateView.as_view(), name='user_avatar'),
    re_path(r'^drf-token-login/', user_views.CustomAuthToken.as_view()),
    # re_path(r'^jwt-token-login/', obtain_jwt_token),
    re_path(r'^jwt-token-login/', user_views.CustomJSONWebToken.as_view()),
    path('weather/', include('apps.weather_search.urls'), name='weather_search')
]


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    re_path(r'ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # path('articles/', article_list, name='article-list'),
    path('api/V1/', include(api_V1_urls)),
]
