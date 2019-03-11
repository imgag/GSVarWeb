import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'
import { parseTSV } from '@/utils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filters: [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat(),
    lines: []
  },
  mutations: {
    replaceLines(state, lines) {
      state.lines = lines
    }
  },
  actions: {
    replaceLinesFromString(state, line) {
      let lines = parseTSV(line)
      state.commit('replaceLines', lines)
    }
  }
})
