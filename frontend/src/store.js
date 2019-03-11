import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filters: [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat()
  },
  mutations: {

  },
  actions: {

  }
})
