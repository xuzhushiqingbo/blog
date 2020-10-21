// 当state中的某些状态在各个组件中都被频繁使用，如果在每个组件中都声明一次，将会变得非常繁琐。
const userInfo = state => {
  return state.userInfo
}

const userName = state => {
  console.log(unescape(state.userInfo.nickname))
  return unescape(state.userInfo.nickname)
}

const userId = state => {
  return state.userInfo.userid
}

const jwtToken = state => {
  return state.userInfo.token
}

export default {
  userInfo, userName, userId, jwtToken
}
