<template>
  <Menu mode="horizontal" theme="dark" active-name="1" @on-select="handleSelect">
    <menu-item name="home">
      <Icon type="ios-paper" />
      网站主页
    </menu-item>
    <menu-item name="blogs">
      <Icon type="ios-people" />
      博客文章
    </menu-item>
    <menu-item name="weather">
      <Icon type="ios-people" />
      天气预报
    </menu-item>
    <menu-item name="users" v-if="userName">
      <Icon type="ios-people" />
      {{userName}}
    </menu-item>
    <menu-item name="logout" v-if="userName">
      <Icon type="ios-construct" />
      退 出
    </menu-item>
    <menu-item name="login" v-if="!userName">
      <Icon type="ios-construct" />
      登 录
    </menu-item>
    <menu-item name="register" v-if="!userName">
      <Icon type="ios-construct" />
      注 册
    </menu-item>
  </Menu>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import cookie from '../store/cookie'

export default {
  name: 'TopNav',
  computed: {
    username () {
      return this.$store.state.userInfo.username
    },
    ...mapState({ username2: (state) => { return state.userInfo.username } }),
    ...mapGetters(['userName'])
  },
  methods: {
    handleSelect (name) {
      if (name === 'home') {
        this.$router.push({ name: 'home' })
      }
      if (name === 'blogs') {
        this.$router.push({ name: 'blog_list' })
      }
      if (name === 'weather') {
        this.$router.push({ name: 'weather' })
      }
      if (name === 'login') {
        this.$router.push({ name: 'user_login' })
      }
      if (name === 'register') {
        this.$router.push({ name: 'user_register' })
      }
      if (name === 'logout') {
        cookie.delCookie('username')
        cookie.delCookie('nickname')
        cookie.delCookie('userid')
        cookie.delCookie('token')
        // 存储,更新 store
        this.$store.dispatch('setInfo')
        // 跳转到登陆页面
        this.$router.push({ name: 'user_login' })
        location.reload()
      }
      if (name === 'users') {
        this.$router.push({ name: 'user_center' })
      }
    }
  }
}
</script>

<style scoped>

</style>
