<template>
<Row>
  <Card>
    <Row :gutter="24">
      <i-col :span="5"><div style="width: 100%;height: 1px"></div></i-col>
      <i-col :span="12">
        <Form :model="pwdForm" :rules="pwdRules" ref="pwdForm" :label-width="100">
          <FormItem label="旧密码" prop="oldPassword">
            <i-input type="password" v-model="pwdForm.oldPassword" auto-complete="off"></i-input>
          </FormItem>
          <FormItem label="新密码" prop="newPassword">
            <i-input type="password" v-model="pwdForm.newPassword" auto-complete="off"></i-input>
          </FormItem>
          <FormItem label="确认密码" prop="checkPassword">
            <i-input type="password" v-model="pwdForm.checkPassword" auto-complete="off"></i-input>
          </FormItem>
          <FormItem label="确认密码" prop="checkPassword">
            <Button type="primary" @click="submitForm2(pwdForm)">提交修改</Button>
            <Button @click="resetForm2(pwdForm)" style="margin-left: 16px">重置表单</Button>
          </FormItem>
        </Form>
      </i-col>
      <i-col :span="7"><div style="width: 100%;height: 1px"></div></i-col>
    </Row>
  </Card>
  <Divider>
   登录账号修改
  </Divider>
  <Card>
    <Row :gutter="24">
      <i-col :span="5"><div style="width: 100%;height: 1px"></div></i-col>
      <i-col :span="12">
        <Form ref="accountForm" :model="accountForm" :label-width="100">
          <FormItem label="手机号">
            <i-input v-model="accountForm.mobile">
              <Button slot="append" @click="handleChangeAccount('mobile')">修改</Button>
            </i-input>
          </FormItem>
          <FormItem label="邮箱">
            <i-input v-model="accountForm.email">
              <Button slot="append" @click="handleChangeAccount('email')">修改</Button>
            </i-input>
          </FormItem>
        </Form>
      </i-col>
      <i-col :span="7"><div style="width: 100%;height: 1px"></div></i-col>
    </Row>
  </Card>
</Row>
</template>

<script>
export default {
  name: 'UserAccount',
  data () {
    let validatePassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入新密码'))
      } else {
        if (this.pwdForm.checkPassword !== '') {
          this.$refs.pwdForm.validateField('checkPassword')
        }
        callback()
      }
    }
    let validatePassword2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.pwdForm.newPassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      pwdForm: {
        oldPassword: '',
        newPassword: '',
        checkPassword: ''
      },
      pwdRules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' }
        ],
        newPassword: [
          { validator: validatePassword, trigger: 'blur' }
        ],
        checkPassword: [
          { validator: validatePassword2, trigger: 'blur' }
        ]
      },
      accountForm: {
        email: '',
        mobile: ''
      }
    }
  },
  methods: {
    submitForm1 (formName) {
      alert('123')
    },
    submitForm2 (formName) {
      alert('456')
    },
    handleChangeAccount (account) {
      if (account === 'email') {
        alert('修改邮箱')
      }
      if (account === 'mobile') {
        alert('修改手机')
      }
    }
  }
}
</script>

<style scoped>

</style>
