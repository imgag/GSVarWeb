import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'

Vue.config.productionTip = false
Vue.prototype.$basePath = 'http://localhost:9000/v1'

new Vue({
  render: h => h(App),
}).$mount('#app')
