import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'
import { parseTSV, produceHeaders } from '@/utils'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filterNames: [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat(),
    lines: [],

    // Loading states
    filterFileLoading: false,
    fileLoaded: false,
    fileLoading: false,

    // Current file and stage
    lastTotalNumberOfVariants: 0,
    lastPath: 0,
    step: 1,

    // Selection
    selectedGenes: []
  },
  getters: {
    headers (state) {
      return (state.lines.length) ? produceHeaders(state.lines.slice(0, 1)[0]) : []
    },
    items (state) {
      return state.lines.slice(1)
    }
  },
  mutations: {
    replaceLines(state, lines) {
      state.lines = lines
    },
    toggleFilterFileLoading(state) {
      state.filterFileLoading = !state.filterFileLoading
    },
    toggleFileLoading (state) {
      state.fileLoading = !state.fileLoading
    },
    setFileLoaded(state) {
      state.fileLoaded = true
    },
    updateLastPath(state, path) {
      state.lastPath = path
    },
    updateLastTotalNumberOfVariants (state, numberOfVariants) {
      state.lastTotalNumberOfVariants = numberOfVariants
    },
    incrementStep(state) {
      state.step = (state.step === 2) ? 1 : 2
    },
    updateSelectedGenes(state, selectedGenes) {
      state.selectedGenes = selectedGenes
    }
  },
  actions: {
    replaceLinesFromString(state, line) {
      let lines = parseTSV(line)
      state.commit('replaceLines', lines)
    }
  }
})
