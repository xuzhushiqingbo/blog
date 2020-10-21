<template>
  <Card style="text-align: center" :padding="64">
    <h3>用户登录</h3>
    <Divider></Divider>
    <Form ref="form" :model="form" :rules="rule" style="width: 50%; margin-left: 25%">
      <FormItem label="请选择一种登陆方式：">
        <RadioGroup v-model="form.manner" size="large">
          <Radio label="username" class="mr-32">用户名</Radio>
          <Radio label="email" class="mr-32">邮箱</Radio>
          <Radio label="mobile" class="mr-32">手机号</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem prop="account">
        <i-input v-if="form.manner==='username'" type="text" v-model="form.account" placeholder="请输入您的用户名" size="large">
          <Icon type="ios-person-outline" size="large" slot="prepend"></Icon>
        </i-input>
        <i-input v-if="form.manner==='email'" type="email" v-model="form.account" placeholder="请输入您的邮箱" size="large">
          <Icon type="ios-person-outline" size="large" slot="prepend"></Icon>
        </i-input>
        <i-input v-if="form.manner==='mobile'" type="text" v-model="form.account" placeholder="请输入您的手机号" size="large">
          <Icon type="ios-person-outline" size="large" slot="prepend"></Icon>
        </i-input>
      </FormItem>
      <FormItem prop="password">
        <i-Input type="password" v-model="form.password" placeholder="请输入密码" size="large">
          <Icon type="ios-lock-outline" size="large" slot="prepend"></Icon>
        </i-Input>
      </FormItem>
      <FormItem>
        <Button type="primary" size="large" @click="handleSubmit('form')" class="mr-32">立即登录</Button>
        <Button type="warning" size="large" @click="gotoRegister('form')" class="mr-32">注册账号</Button>
        <Button type="error" size="large" @click="findPassword('form')">找回密码</Button>
      </FormItem>
    </Form>
  </Card>
</template>

<script>
import { userLogin } from '../api/api'
import cookie from '../store/cookie'

export default {
  name: 'UserLogin',
  data () {
    const validateAccount = (rule, value, callback) => {
      if (value === '') {
        if (this.form.manner === 'username') {
          callback(new Error('请输入您的用户名'))
        }
        if (this.form.manner === 'email') {
          callback(new Error('请输入您的邮箱'))
        }
        if (this.form.manner === 'mobile') {
          callback(new Error('请输入您的手机号'))
        }
      } else {
        if (this.form.manner === 'email') {
          if (this.form.account.indexOf('@') === -1) {
            callback(new Error('请输入正确的邮箱格式'))
          }
        }
        if (this.form.manner === 'mobile') {
          if (this.form.account.length !== 11) {
            callback(new Error('手机号码必须是11位！'))
          }
          if (!(/^1(3|5|7|8)\d{9}$/.test(this.form.account))) {
            callback(new Error('手机号码格式不正确！'))
          }
        }
        callback()
      }
    }
    return {
      form: {
        manner: 'username',
        account: '',
        password: ''
      },
      rule: {
        account: [
          { validator: validateAccount, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请填入你的登陆密码', trigger: 'blur' },
          { type: 'string', min: 6, message: '密码不能小于6个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$Message.success('正在登陆')
          userLogin({ username: this.form.account, password: this.form.password }).then(
            (response) => {
              console.log(response.data)
              cookie.setCookie('username', response.data.username)
              cookie.setCookie('nickname', response.data.nickname)
              cookie.setCookie('userid', response.data.userid)
              cookie.setCookie('token', response.data.token)
              // 存储,更新 store
              this.$store.dispatch('setInfo')
              // 登陆成功，跳转到首页
              this.$router.push({ name: 'home' })
            }
          ).catch((error) => {
            this.$Message.error('信息填写错误')
            console.log(error.response)
          })
        } else {
          this.$Message.error('表单验证失败！')
        }
      })
    },
    gotoRegister (name) {
      this.$Message.success('去注册!')
    },
    findPassword (name) {
      this.$Message.success('找回密码!')
    }
  }
}
</script>

<style scoped>
  .mr-32 {
    margin-right: 32px;
  }
</style>
