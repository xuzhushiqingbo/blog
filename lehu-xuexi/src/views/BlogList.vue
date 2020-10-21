<template>
<Row :gutter="16">
    <i-col :span="17">
      <Card :padding="8" class="mb-8">
        <Button class="mctg" shape="circle" size="default" @click="handleSelectCategory('所有分类')">所有分类</Button>
        <Button class="mctg" shape="circle" size="small" v-for="(item, index) in categories" :key="index"
                @click="handleSelectCategory(item)">{{item.name}}</Button>
        <hr style="margin: 4px 0"/>
        <Button class="mctg" shape="circle" size="default" @click="handleSelectOrder('默认排序')">默认排序</Button>
        <Button class="mctg" shape="circle" size="small" @click="handleSelectOrder('add_time')">发布时间</Button>
        <Button class="mctg" shape="circle" size="small" @click="handleSelectOrder('click_num')">浏览量</Button>
        <Button class="mctg" shape="circle" size="small" @click="handleSelectOrder('comment_num')">评论量</Button>
        <Button class="mctg" shape="circle" size="small" @click="handleSelectOrder('favor_num')">收藏量</Button>
      </Card>
      <Row>
        <article-card v-for="(item,index) in articles" :key="index" :article="item"
                      @category-click="handleCategoryClick" @tag-click="handleTagClick"></article-card>
        <Card style="text-align: center">
          <Page :total="articleCount" :page-size="10" show-sizer show-total show-elevator
                @on-change="handlePagination" @on-page-size-change="handlePageSizeChange"/>
        </Card>
      </Row>
    </i-col>
    <i-col :span="7">
      <Card class="mb-8" :padding="8"><Button type="primary" @click="handleCreateBlog">写博客</Button></Card>
      <Card :padding="8">
        <p slot="title">
          <Icon type="ios-film-outline"></Icon>
          博客标签
        </p>
        <a href="#" slot="extra" @click.prevent="changeLimit">
          <Icon type="ios-loop-strong"></Icon>
          更多标签
        </a>
        <Button class="mctg" shape="circle" size="small" @click="handleSelectTags('所有标签')">所有标签</Button>
        <Button class="mctg" shape="circle" size="small" v-for="(item, index) in tags" :key="index"
                @click="handleSelectTags(item)">{{item.name}}</Button>
      </Card>
    </i-col>
</Row>
</template>

<script>
import { getBlogCategories, getBlogTags, getBlogArticles } from '../api/api'
import ArticleCard from '../components/ArticleCard'
export default {
  name: 'BlogList',
  components: { ArticleCard },
  data () {
    return {
      categories: ['Django专题', 'Tornado专题', 'Flask专题', 'Python专题', 'Element专题', 'PyTorch专题'],
      tags: ['django', 'tornado', 'flask', 'python', 'element', 'pytorch'],
      tagCount: 0,
      taglimit: 10,
      articles: [],
      articleCount: 0,
      descend: false,
      filterParams: {
        category: null,
        tags: null,
        user: null,
        title: null,
        click_min: null,
        click_max: null,
        favor_min: null,
        comment_min: null,
        ordering: null,
        page: null,
        page_size: null
      }
    }
  },
  methods: {
    obtainBlogCategories: function () {
      getBlogCategories({}).then(
        (response) => {
          this.categories = response.data
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    obtainBlogTags: function (taglimit, tagoffset) {
      getBlogTags({ params: { limit: taglimit, offset: tagoffset } }).then(
        (response) => {
          this.tags = response.data.results
          this.tagsCount = response.data.count
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    obtainBlogArticles (queryParams) {
      getBlogArticles({ params: queryParams }).then(
        (response) => {
          this.articles = response.data.results
          this.articleCount = response.data.count
        }
      ).catch((error) => {
        console.log(error.response)
      })
    },
    changeLimit () {
      this.taglimit = this.tagsCount
      this.obtainBlogTags(this.taglimit, 0)
    },
    handleSelectCategory (category) {
      this.filterParams.category = category === '所有分类' ? null : category.id
      this.filterParams.tags = null
      this.obtainBlogArticles(this.filterParams)
    },
    handleSelectOrder (order) {
      this.descend = !this.descend
      let ordering = order === '默认排序' ? null : order
      if (ordering) {
        if (this.descend && !ordering.startsWith('-')) {
          ordering = '-' + ordering
        }
      }
      this.filterParams.ordering = ordering
      this.obtainBlogArticles(this.filterParams)
    },
    handleSelectTags (tag) {
      this.filterParams.tags = tag === '所有标签' ? null : tag.id
      this.obtainBlogArticles(this.filterParams)
    },
    handleCategoryClick (param) {
      this.handleSelectCategory(param.category)
    },
    handleTagClick (param) {
      this.handleSelectTags(param.tag)
    },
    handlePagination (page) {
      this.filterParams.page = page
      this.obtainBlogArticles(this.filterParams)
    },
    handlePageSizeChange (pageSize) {
      this.filterParams.page_size = pageSize
      this.obtainBlogArticles(this.filterParams)
    },
    handleCreateBlog () {
      this.$router.push({ name: 'blog_create' })
    }
  },
  mounted () {
    this.obtainBlogCategories()
    this.obtainBlogTags(this.taglimit, 0)
    this.obtainBlogArticles(this.filterParams)
  }
}
</script>

<style scoped>
 .mctg{
   margin-right: 4px;
   margin-bottom: 4px;
 }
 .mb-8 {
   margin-bottom: 8px;
 }
</style>
