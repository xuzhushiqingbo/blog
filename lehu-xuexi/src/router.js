import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Weather from './views/Weather'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/user/login',
      name: 'user_login',
      component: () => import('./views/UserLogin.vue')
    },
    {
      path: '/user/register',
      name: 'user_register',
      component: () => import('./views/UserRegister.vue')
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/blog/list',
      name: 'blog_list',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/BlogList.vue')
    },
    {
      path: '/blog/:ctg/:aid/',
      name: 'blog_detail',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/BlogDetail.vue')
    },
    {
      path: '/blog/create/',
      name: 'blog_create',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/BlogCreate.vue')
    },
    {
      path: '/user/center/',
      name: 'user_center',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/UserCenter.vue'),
      redirect: '/user/center/info/',
      children: [
        {
          path: 'info',
          name: 'user_info',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "about" */ './views/UserInfo.vue')
        },
        {
          path: 'account',
          name: 'user_account',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "about" */ './views/UserAccount.vue')
        },
        {
          path: '/weather',
          name: 'weather',
          component: Weather
        }
      ]
    }
  ]
})
