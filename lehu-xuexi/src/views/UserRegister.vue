<template>
  <Card style="text-align: center" :padding="64">
    <h3>用户注册</h3>
    <Divider></Divider>
    <Form ref="form" :model="form" :rules="rule" style="width: 50%; margin-left: 25%">
      <FormItem label="请选择一种注册方式：">
        <RadioGroup v-model="form.manner" size="large">
          <Radio label="email" class="mr-32">邮箱</Radio>
          <Radio label="mobile" class="mr-32">手机号</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem prop="account">
        <i-input v-if="form.manner==='email'" type="email" v-model="form.account" placeholder="请输入您的邮箱" size="large">
          <span type="text" slot="prepend">邮 箱：</span>
        </i-input>
        <i-input v-if="form.manner==='mobile'" type="text" v-model="form.account" placeholder="请输入您的手机号" size="large">
          <span type="text" slot="prepend">手 机：</span>
        </i-input>
      </FormItem>
      <FormItem prop="code">
        <i-input type="text" v-model="form.code" placeholder="请输入您收到的验证码" size="large">
          <Button type="primary" slot="prepend" :loading="loading" @click="handleSendVerifyCode">
            <span v-if="!loading">点击获取验证码</span>
            <span v-else>5分钟后可重发</span>
          </Button>
        </i-input>
      </FormItem>
      <FormItem prop="username">
        <i-input type="text" v-model="form.username" placeholder="请输入您的用户名" size="large">
          <span type="text" slot="prepend">用户名：</span>
        </i-input>
      </FormItem>
      <FormItem prop="password">
        <i-Input type="password" v-model="form.password" placeholder="请输入密码" size="large">
          <span type="text" slot="prepend">密 码：</span>
        </i-Input>
      </FormItem>
      <FormItem prop="passwordCheck">
        <i-input type="password" v-model="form.passwordCheck" placeholder="请再次输入密码" size="large">
          <span type="text" slot="prepend">确认密码：</span>
        </i-input>
      </FormItem>
      <FormItem>
        <Button type="primary" size="large" @click="handleSubmit('form')" class="mr-32">立即注册</Button>
        <Button type="warning" size="large" @click="gotoLogin('form')" class="mr-32">已有账号</Button>
      </FormItem>
    </Form>
  </Card>
</template>

<script>
import { getVerifyCode, userRegister } from '../api/api'
import cookie from '../store/cookie'

export default {
  name: 'UserRegister',
  data () {
    const validateAccount = (rule, value, callback) => {
      if (value === '') {
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
    const validateUsername = (rule, value, callback) => {
      // 模拟异步验证效果
      setTimeout(() => {
        if (value.length < 3) {
          callback(new Error('用户名至少为3个字符'))
        } else {
          if (value.length > 20) {
            callback(new Error('用户名不能超过20个字符'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入您的密码！'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不能小于6个字符！'))
      } else {
        if (this.form.passwordCheck !== '') {
          // 对第二个密码框单独验证
          this.$refs.form.validateField('passwordCheck')
        }
        callback()
      }
    }
    const validatePasswordCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入你的密码！'))
      } else if (value !== this.form.password) {
        callback(new Error('两次输入的密码不匹配!'))
      } else {
        callback()
      }
    }
    return {
      loading: false,
      form: {
        manner: 'email',
        account: '',
        code: '',
        username: '',
        password: '',
        passwordCheck: ''
      },
      rule: {
        account: [
          { validator: validateAccount, trigger: 'blur' }
        ],
        code: [
          { required: true, message: '请填入你收到的验证码', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请填入你的用户名', trigger: 'blur' },
          { validator: validateUsername, trigger: 'blur' }
        ],
        password: [
          { validator: validatePassword, trigger: 'blur' }
        ],
        passwordCheck: [
          { validator: validatePasswordCheck, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          userRegister({
            account_type: this.form.manner,
            account: this.form.account,
            password: this.form.password,
            code: this.form.code,
            username: this.form.username }).then(
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
              this.$Message.success('注册成功!')
            }
          ).catch((error) => {
            console.log(error.response)
            if (error.response.status === 400) {
              if (error.response.data.username) {
                alert(error.response.data.username)
              }
              if (error.response.data.code) {
                alert(error.response.data.code)
              }
            }
          })
        } else {
          this.$Message.error('注册失败!')
        }
      })
    },
    handleSendVerifyCode () {
      if (this.form.account === '') {
        alert('邮箱或手机号不能为空!')
        return
      }
      this.loading = true
      // 过一段时间再次允许重新发送
      setTimeout(() => {
        if (this.loading) {
          this.loading = false
        }
      }, 2000)
      getVerifyCode({ account_type: this.form.manner, account: this.form.account }).then(
        (response) => {
          console.log(response.data)
          this.$Message.success('验证码已发送成功!')
        }
      ).catch((error) => {
        console.log(error.response)
        if (error.response.data.non_field_errors) {
          alert(error.response.data.non_field_errors)
        }
      })
    },
    gotoLogin (name) {
      this.$Message.success('去登录!')
    }
  }
}
</script>

<style scoped>
  .mr-32 {
    margin-right: 32px;
  }
</style>
