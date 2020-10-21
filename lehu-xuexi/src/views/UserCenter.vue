<template>
  <Row>
    <hr/>
    <Row :gutter="16" type="flex" justify="center">
      <!--<i-col :span="4">-->
      <!--<Menu mode="vertical" width="auto" theme="light" active-name="activeName" @on-select="handleSelect">-->
        <!--<MenuGroup title="个人信息管理">-->
          <!--<MenuItem name="user-info">-->
            <!--<Icon type="md-document" />-->
            <!--基本信息管理-->
          <!--</MenuItem>-->
          <!--<MenuItem name="user-account">-->
            <!--<Icon type="md-chatbubbles" />-->
            <!--个人账号管理-->
          <!--</MenuItem>-->
        <!--</MenuGroup>-->
        <!--<MenuGroup title="个人内容管理">-->
          <!--<MenuItem name="user-articles">-->
            <!--<Icon type="md-document" />-->
            <!--发表文章管理-->
          <!--</MenuItem>-->
          <!--<MenuItem name="user-comments">-->
            <!--<Icon type="md-chatbubbles" />-->
            <!--发表评论管理-->
          <!--</MenuItem>-->
        <!--</MenuGroup>-->
        <!--<MenuGroup title="其他内容管理">-->
          <!--<MenuItem name="favor-articles">-->
            <!--<Icon type="md-heart" />-->
            <!--收藏的文章管理-->
          <!--</MenuItem>-->
          <!--<MenuItem name="user-courses">-->
            <!--<Icon type="md-leaf" />-->
            <!--学习课程管理-->
          <!--</MenuItem>-->
        <!--</MenuGroup>-->
      <!--</Menu>-->
      <!--</i-col>-->
      <i-col :span="20">
        <router-view></router-view>
      </i-col>
    </Row>
  </Row>
</template>

<script>
// import UserInfo from './UserInfo'
export default {
  name: 'UserCenter',
  // components: { UserInfo },
  computed: {
    activeName () {
      let path = this.$refs.path
      if (path.indexOf('info') !== -1) return 'user-info'
      if (path.indexOf('account') !== -1) return 'user-account'
      return 'user-info'
    }
  },
  methods: {
    handleSelect (name) {
      if (name === 'user-info') {
        this.$router.push({ name: 'user_info' })
      }
      if (name === 'user-account') {
        this.$router.push({ name: 'user_account' })
      }
    }
  }
}
</script>

<style scoped>

</style>
