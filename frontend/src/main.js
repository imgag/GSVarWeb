import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false
Vue.prototype.$basePath = 'http://localhost:9000/v1'

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
