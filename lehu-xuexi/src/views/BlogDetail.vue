<template>
  <Row :gutter="16">
    <i-col :span="17">
      <Card v-if="article">
        <h2>{{article.title}}<small style="float: right">{{article.add_time.split('T')[0]}}</small></h2>
        <hr style="margin: 8px 0"/>
        <Row>
          <Divider type="vertical"></Divider>
          <span>收藏量: {{article.favor_num}}</span>
          <Divider type="vertical"></Divider>
          <span>评论量: {{article.comment_num}}</span>
          <Divider type="vertical"></Divider>
          <span>阅读量: {{article.click_num}}</span>
          <Button type="primary" style="float: right">收藏</Button>
          <Button type="info" style="float: right;margin-right: 8px">分享</Button>
        </Row>
        <hr style="margin: 8px 0"/>
      <div v-if="article" v-html="article.content">
        {{article.content}}
      </div>
      </Card>
    </i-col>
    <i-col :span="7">
        <Card style="width:100%" v-if="article">
            <div style="text-align:center">
              <img :src="article.user.avatar">
              <h3>作者：{{article.user.nickname}}</h3>
            </div>
          </Card>
          <Card style="width:100%; margin-top: 8px" v-if="article">
            <p slot="title">
              文章推荐
            </p>
            <ul style="list-style: none">
              <li v-for="(item, index) in relatedArticleList" :key="index">
                <article-simple-card :article="item"></article-simple-card>
              </li>
            </ul>
            <p slot="extra">
              <span style="margin-right: 8px" @click="obtainBlogArticles('user')">同作者</span>
              <span @click="obtainRelatedArticles('category')">同类别</span>
            </p>
            <ul style="list-style:none;">
              <li v-for="(item, index) in relatedArticleList" :key="index">
                <article-simple-card :article="item"></article-simple-card>
              </li>
            </ul>
          </Card>
    </i-col>
  </Row>
</template>

<script>
import { getArticleDetail, getBlogArticles } from '../api/api'
import ArticleSimpleCard from '../components/ArticleSimpleCard'
export default {
  name: 'BlogDetail',
  components: { ArticleSimpleCard },
  comments: {
    ArticleSimpleCard
  },
  data () {
    return {
      articleId: null,
      article: null,
      relatedArticleList: []
    }
  },
  methods: {
    obtainArticleDetail (articleId) {
      getArticleDetail({ id: articleId }).then(
        (response) => {
          this.article = response.data
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    obtainBlogArticles (queryParams) {
      getBlogArticles({ params: queryParams }).then(
        (response) => {
          this.relatedArticleList = response.data.results
          // this.articleCount = response.data.count
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    obtainRelatedArticles (param) {
      if (param.category) {
        this.obtainBlogArticles(param)
      }
      if (param === 'user') {
        this.obtainBlogArticles({ user: this.article.user.id })
      }
      if (param === 'category') {
        this.obtainBlogArticles({ category: this.article.category.id })
      }
    }
  },
  mounted () {
    this.articleId = this.$route.params.aid
    this.obtainArticleDetail(this.articleId)
    this.obtainRelatedArticles({ category: this.$route.params.ctg })
  }
}
</script>

<style scoped>

</style>
