/* eslint-disable */

import axios from 'axios'

// 全局状态控制引入
import store from '../store/store'

//
// http request 拦截器
axios.interceptors.request.use(
  config => {
    if (store.state.userInfo.token) {
      // 判断是否存在token，如果存在的话，则每个http header都加上token
      config.headers.Authorization = `JWT ${store.state.userInfo.token}`
    }
    return config
  },
  err => {
    return Promise.reject(err)
  })
