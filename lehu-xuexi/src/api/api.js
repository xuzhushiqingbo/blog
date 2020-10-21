import axios from 'axios'

let host = 'http://127.0.0.1:8000/api/V1'

// 验证码
export const getVerifyCode = params => { return axios.post(`${host}/verifycodes/`, params) }

// 注册
export const userRegister = params => { return axios.post(`${host}/register/`, params) }

// 登录
export const userLogin = params => { return axios.post(`${host}/jwt-token-login/`, params) }

// 获取用户详情
export const getUserDetail = params => { return axios.get(`${host}/users/${params.id}/`) }

// 更新用户详情
export const updateUserDetail = params => { return axios.patch(`${host}/users/${params.id}/ `, params) }

// 更新用户头像
export const updateUserAvatar = params => { return axios.post(`${host}/user/avatar/ `, params) }

// 获取博客数据
export const getBlogCategories = params => { return axios.get(`${host}/categories/`, params) }

// 获取博客标签
export const getBlogTags = params => { return axios.get(`${host}/tags/`, params) }

// 获取博客文章列表
export const getBlogArticles = params => { return axios.get(`${host}/articles/`, params) }

// 获取博客文章详情
export const getArticleDetail = params => { return axios.get(`${host}/articles/${params.id}/`) }

// 创建博客文章
export const createArticle = params => { return axios.post(`${host}/article/create/`, params) }

// 上传图片
export const createArticleImage = params => { return axios.post(`${host}/article/images/create/`, params) }

// 创建文章插图
export const postArticleImage = params => { return axios.post(`${host}/article/image/`, params) }

// 获取城市
export const getCityWeather = params => { return axios.get(`${host}/weather/get_select/${params}`) }

// 获取地区
export const getAreaWeather = params => { return axios.get(`${host}/weather/get_picture/${params}`) }

// 获取天气
export const searchWeather = params => { return axios.get(`${host}/weather/search_weather/${params}`) }
