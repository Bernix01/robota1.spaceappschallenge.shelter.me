import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
process.env.GOOGLE_API_KEY = 'AIzaSyDm5y69ZnedXOyK2YWxieluzQSDf354vCg'
Vue.http = Vue.prototype.$http = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000,
  headers: {'X-Custom-Header': 'foobar'}
})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
