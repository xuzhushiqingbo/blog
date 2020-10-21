import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'
import './api/axios'
import './plugins/iview'
import './plugins/mavoneditor'
import './plugins/vuequilleditor'


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
