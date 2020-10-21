from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import UserSimpleSerializer
from blogs.models import Article, BlogCategory, BlogTag, ArticleImage

User = get_user_model()


# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=150)
#     content = serializers.CharField(style={'base_template': 'textarea.html'})
#     click_num = serializers.IntegerField(default=0)
#     add_time = serializers.DateTimeField()
#     cover = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Article` instance, given the validated data.
#         """
#         return Article.objects.create(**validated_data)
from users.serializers import UserSimpleSerializer


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        # fields = ['id', 'title', 'category', 'brief', 'content', 'click_num', 'cover', 'add_time']
        fields = ['name', 'id']


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        # fields = ['id', 'title', 'category', 'brief', 'content', 'click_num', 'cover', 'add_time']
        fields = ['name', 'id']


class ArticleSimpleSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer()
    tags = BlogTagSerializer(many=True)
    user = UserSimpleSerializer()

    class Meta:
        model = Article
        fields = ['id', 'category', 'brief', 'tags', 'user', 'title', 'brief', 'click_num', 'cover', 'comment_num',
                  'favor_num', 'add_time']


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer()
    tags = BlogTagSerializer(many=True)
    user = UserSimpleSerializer()

    class Meta:
        model = Article
        # fields = ['id', 'title', 'category', 'brief', 'content', 'click_num', 'cover', 'add_time']
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    # def validate(self, attrs):
    #
    #     userid = int(self.initial_data['user'])
    #     attrs['user'] = User.objects.get(id=userid)
    #     return attrs

    class Meta:
        model = Article
        fields = ['id', 'add_time', 'category', 'tags', 'user', 'title', 'cover', 'brief', 'content']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['image']