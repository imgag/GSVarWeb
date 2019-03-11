import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'
import { parseTSV, produceHeaders } from '@/utils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filterNames: [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat(),
    lines: [],
    filterFileLoading: false,
    fileLoaded: false,
    lastTotalNumberOfVariants: 0,
    lastPath: 0
  },
  getters: {
    headers (state) {
      return produceHeaders(state.lines.slice(0, 1)[0])
    },
    items (state) {
      return state.lines.slice(1)
    }
  },
  mutations: {
    updateLastPath(state, path) {
      state.lastPath = path
    },
    updateLastTotalNumberOfVariants (state, numberOfVariants) {
      state.lastTotalNumberOfVariants = numberOfVariants
    },
    toggleFilterFileLoading(state) {
      state.filterFileLoading = !state.filterFileLoading
    },
    setFileLoaded(state) {
      state.fileLoaded = true
    },
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
