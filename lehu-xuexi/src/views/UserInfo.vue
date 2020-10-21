<template>
<Row :gutter="35" type="flex" justify="center">
  <i-col :span="12">
    <Card>
      <Form ref="formValidate" :model="formValidate" :rules="formValidate" :lable-width="100">
        <FormItem label="用户名">
          <i-input type="text" v-model="formValidate.username" readonly></i-input>
        </FormItem>
        <FormItem label="手机号">
          <i-input type="text" v-model="formValidate.mobile" readonly></i-input>
        </FormItem>
        <FormItem label="邮箱">
          <i-input type="email" v-model="formValidate.email" readonly></i-input>
        </FormItem>
        <FormItem label="昵称" prop="nickname">
          <i-input type="text" v-model="formValidate.nickname"></i-input>
        </FormItem>
        <FormItem label="地址" prop="address">
          <i-input type="text" v-model="formValidate.address"></i-input>
        </FormItem>
        <FormItem label="性别" prop="gender">
          <RadioGroup v-model="formValidate.gender">
            <Radio label="male">男</Radio>
            <Radio label="female">女</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="生日" prop="birthday">
          <i-input type="text" v-model="formValidate.birthday"></i-input>
        </FormItem>
        <FormItem label="个人简介" prop="introduction">
          <i-input type="textarea" v-model="formValidate.introduction" :autosize="{minRows: 2,maxRows: 5}" placeholder="请输入个人简介"></i-input>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="handleSubmit('formValidate')">提交修改</Button>
        </FormItem>
      </Form>
    </Card>
  </i-col>
  <i-col :span="9" style="text-align: center">
    <Card>
      <div>
        <img :src="formValidate.avatar" style="width: 300px;height: 300px"/>
      </div>
      <Upload name="avatar"
      :before-upload="handleUpload"
              :on-success="handleSuccess"
              :headers="headers"
      action="http://127.0.0.1:8000/api/V1/user/avatar/">
        <Button icon="ios-cloud-upload-outline">上传头像文件</Button>
      </Upload>
      <div v-if="file !== null">将要上传的文件: {{file.name}} <Button type="primary" @click="upload" :loading="loadingStatus">{{ loadingStatus ? '正在上传中' : '点击这里上传' }}</Button></div>
    </Card>
  </i-col>
</Row>
</template>

<script>
import { getUserDetail, updateUserAvatar, updateUserDetail } from '../api/api'
import { mapGetters } from 'vuex'

export default {
  name: 'UserInfo',
  data () {
    return {
      formValidate: {
        username: '',
        email: '',
        mobile: '',
        nickname: '',
        gender: '',
        avatar: '',
        introduction: '',
        address: '',
        birthday: ''
      },
      ruleValidate: {
      },
      file: null,
      loadingStatus: false
    }
  },
  computed: {
    ...mapGetters(['userId']),
    ...mapGetters(['jwtToken']),
    headers () {
      return { Authorization: `JWT ${this.jwtToken}` }
    }
  },
  methods: {
    // dateFormat (date) {
    //   Date.prototype.format = function (fmt) {
    //     let o = {
    //       'M+': this.getMonth() + 1, // 月份
    //       'd+': this.getDate(), // 日
    //       'h+': this.getHours(), // 小时
    //       'm+': this.getMinutes(), // 分
    //       's+': this.getSeconds(), // 秒
    //       'q+': Math.floor((this.getMonth() + 3) / 3), // 季度
    //       'S': this.getMilliseconds() // 毫秒
    //     }
    //     if (/(y+)/.test(fmt)) {
    //       fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length))
    //     }
    //     for (let k in o) {
    //       if (new RegExp('(' + k + ')').test(fmt)) {
    //         fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
    //       }
    //     }
    //     return fmt
    //   }
    //   let newDate = date.format('yyyy-MM-dd')
    //   return newDate
    // },
    obtainUserDetail (userid) {
      getUserDetail({ id: userid }).then((response) => {
        console.log(response.data)
        this.formValidate = response.data
      }).catch((error) => {
        console.log(error.response)
      })
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          // this.formValidate.avatar = this.file
          updateUserDetail(this.formValidate).then((response) => {
            this.formValidate = response.date
            this.$Message.success('更新成功！')
          }).catch((error) => {
            console.log(error.response)
          })
        } else {
          this.$Message.error('失败')
        }
      })
    },
    handleUpload (file) {
      this.file = file
      return false
    },
    upload () {
      this.loadingStatus = true
      let formData = new FormData()
      formData.append('avatar', this.file)
      updateUserAvatar(formData).then((response) => {
        this.formValidate.avatar = response.data.avatar
        this.file = null
        this.loadingStatus = false
        this.$Message.success('Success')
      }
      ).catch((error) => {
        console.log(error.response)
        if (error.response.status === 400) {
          if (error.response.data.avatar) {
            alert(error.response.data.avatar)
          }
        }
        this.loadingStatus = false
        this.file = null
      })
      // setTimeout(() => {
      //   this.file = null
      //   this.loadingStatus = false
      //   this.$Message.success('Success')
      // }, 1500)
    },
    handleSuccess (res, file) {
      this.formValidate.avatar = res.avatar
      console.log(res)
      console.log(file)
    }
  },
  created () {
    if (this.userId) {
      this.obtainUserDetail(this.userId)
    }
  }
}
</script>

<style scoped>

</style>
