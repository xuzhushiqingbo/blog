from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(filters.FilterSet):

    click_min = filters.NumberFilter(field_name="click_num", lookup_expr='gte')
    click_max = filters.NumberFilter(field_name="click_num", lookup_expr='lte')
    favor_min = filters.NumberFilter(field_name="favor_num", help_text="最低收藏了", lookup_expr='gte')
    comment_min = filters.NumberFilter(field_name="comment_num", help_text='最低评论量', lookup_expr='gte')
    title = filters.CharFilter(field_name='title', help_text='模糊查询', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['category', 'tags', 'user', 'title', 'click_min', 'click_max', 'favor_min', 'comment_min']
