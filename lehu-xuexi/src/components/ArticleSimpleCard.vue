<template>
  <Card v-if="article" class="mb-8" :padding="4">
    <Row :gutter="8">
      <i-col :span="10">
        <img :src="article.cover" class="cover-image" @click="gotoArticleDetail"/>
      </i-col>
      <i-col :span="14">
        <router-link :to="'/blog/'+ article.category.id + '/' + article.id" target="_blank"><h3>{{article.title}}</h3></router-link>
      </i-col>
    </Row>
  </Card>
</template>

<script>
export default {
  name: 'ArticleSimpleCard',
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
      this.$router.push({ name: 'blog_detail', params: { aid: this.article.id, ctg: this.article.category.id } })
      this.$router.go(0)
    }
  }
}
</script>

<style scoped>
  .mb-8 {
    margin-bottom: 8px;
  }
  .cover-image {
    height: 100px;
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
