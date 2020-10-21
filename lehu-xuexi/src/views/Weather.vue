/**
1.一个搜索框
2.分栏，4X3
3.放置图片，
4.进度条
*/

<template>
  <div>
    <Card>
      <!-- 搜索框 -->
      <Row type='flex' justify='center'>
        <i-col span='8'>
          <Input search enter-button autofocus placeholer='输入' @on-enter="searchDemo()" size="large" v-model="city"/>
          <!-- <i-input type='text' icon='ios-search' size='large' placeholder='请输入您想要查找的城市' :value.sync='city' @on-enter="search('1222')"></i-input> -->
        </i-col>
      </Row>
      <!-- 显示城区 -->
      <!--<Row type='flex' justify='start' class='code-row-bg' :gutter="15">-->
        <!--<i-col span='6' v-for="(val,key,i) in area" :key='i'>-->
          <!--<Icon type="md-pin" size="20" />-->
          <!--<p><a href="javascript:void(0);" @click="areaWeather(`${key}`)">{{val}}</a></p>-->
        <!--</i-col>-->
      <!--</Row>-->
      <!-- 当地天气预报 -->
      <Row type='flex' justify='center'>
        <i-col span='12'>
          <!-- <img :src="`${this.img}`" alt="" style="width:600px;height:300px"> -->
          <img :src="img" alt="" style="width:600px;height:300px">
        </i-col>
      </Row>
    </Card>
  </div>
</template>

<script>
import { getCityWeather, getAreaWeather, searchWeather } from '../api/api'
export default {
  name: 'Weather',
  data () {
    return {
      city: '',
      area: {},
      areaNumber: '',
      img: ''
    }
  },
  methods: {
    search () {
      getCityWeather(this.city)
        .then((res) => {
          console.log(res.data)
          this.area = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
    areaWeather (param) {
      param = this.city + '/' + param
      getAreaWeather(param)
        .then((res) => {
          console.log(res)
          this.img = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
    searchDemo () {
      searchWeather(this.city)
        .then((res) => {
          console.log(res)
          this.img = res.data
        })
    }
  }
}
</script>

<style scope>
p>a{
  color: rgb(56, 47, 44)
}
</style>
