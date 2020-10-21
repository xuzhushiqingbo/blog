<template>
  <Card v-if="article" class="mb-8" :padding="4">
    <Row :gutter="8">
      <i-col :span="6">
        <img :src="article.cover" class="cover-image" @click="gotoArticleDetail"/>
      </i-col>
      <i-col :span="18">
        <h3>{{article.title}}</h3>
        <p class="brief">{{article.brief}}</p>
        <p class="info">分类:
          <Button shape="circle" size="small" type="error" @click="handleClickCategory">{{article.category.name}}</Button>
        </p>
        <p class="info">标签:
          <span v-for="(tag,index) in article.tags" :key="index" style="margin-right: 8px" @click="handleClickTags(tag)">
            <Badge type="warning"  :text="tag.name"></Badge>
          </span>
        </p>
        <p class="info time">{{article.user.nickname}} 发表于 {{article.add_time.split('T')[0]}} </p>
      </i-col>
    </Row>
  </Card>
</template>

<script>
export default {
  name: 'ArticleCard',
  props: {
    article: null
  },
  methods: {
    handleClickCategory () {
      this.$emit('category-click', { category: this.article.category })
    },
    handleClickTags (tag) {
      this.$emit('tag-click', { tag: tag })
    },
    gotoArticleDetail () {
      // this.$router.push({ name: 'blog_detail', params: { aid: this.article.id, ctg: this.article.category.id } })
      this.$router.push({ name: 'blog_detail', params: { aid: this.article.id, ctg: this.article.category.id } })
    }
  }
}
</script>

<style scoped>
  .mb-8 {
    margin-bottom: 8px;
  }
  .cover-image {
    height: 160px;
    width: 100%
  }
  .brief {
    margin-left: 16px;
    margin-right: 8px;
    margin-top: 8px;
  }
  .info {
    margin-top: 8px;
  }
  .time {
    float: right;
  }
</style>
