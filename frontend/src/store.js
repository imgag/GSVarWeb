import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'
import { parseTSV, produceHeaders, fileNameFromPath, createFilterConfig } from '@/utils'

Vue.use(Vuex)

const $basePath = 'http://localhost:9000/v1'

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
    /**
     * Parses lines
     * @function
     * @param context
     * @param line
     */
    replaceLinesFromString(context, line) {
      let lines = parseTSV(line)
      context.commit('replaceLines', lines)
    },
    /**
     * Uploads a GSVar file to the server
     * @function
     * @param {Object} context
     * @param {File} file
     * @return {Promise<any>}
     */
    uploadGSVarFile (context, file) {
      return new Promise((resolve, reject) => {
        let formData = new FormData()
        formData.append('uploadedFile', file.files[0])
        let xhr = new XMLHttpRequest()
        xhr.open('POST', `${$basePath}/upload`, true)
        xhr.onload = () => {
          if (xhr.status === 200) {
            resolve(xhr.statusText)
          } else {
            reject(xhr.statusText)
          }
        }
        xhr.send(formData)
      })
    },
    /**
     * Loads a file from path
     * @function
     * @param context
     * @param path
     * @return {Promise<any>}
     */
    loadGSVarFileFromPath (context, path) {
      return new Promise((resolve, reject) => {
        let fileName = fileNameFromPath(path)
        fetch(`${$basePath}/download/truncated/${fileName}`).then((response) => {
          if (response.status === 200) {
            response.text().then((line) => {
              context.dispatch('replaceLinesFromString', line)
              context.commit('setFileLoaded')
              resolve(response.statusText)
            })
          } else {
            reject(response.statusText)
          }
        })
      })
    },
    /**
     *
     * @param context
     * @param file
     */
    updateSelectedFile(context, file) {
      if (context.state.lastPath !== file.value) {
        context.commit('toggleFileLoading')
        context.dispatch('uploadGSVarFile', file).then(() => {
          context.dispatch('loadGSVarFileFromPath', file.value).then(() => {
            context.commit('updateLastPath', file.value)
            context.commit('updateLastTotalNumberOfVariants', context.state.lines.length)
            context.commit('incrementStep')
            context.commit('toggleFileLoading')
          })
        })
      } else {
        context.commit('incrementStep')
      }
    },
    applyFilter (context, name) {
      let config = createFilterConfig(filterJSON, name)
      let dateAppend = String(Date.now())
      let outFile = context.state.lastPath.replace('.GSvar', `_${dateAppend}.GSVar`)
      context.commit('toggleFilterFileLoading')

      fetch(`${$basePath}/VariantFilterAnnotations`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          in: fileNameFromPath(context.state.lastPath),
          out: fileNameFromPath(outFile),
          filter: config
        })
      }).then(() => {
        context.dispatch('loadGSVarFileFromPath', outFile)
        context.commit('toggleFilterFileLoading')
      }).catch((err) => {
        console.error(err) // eslint-disable-line
        context.commit('toggleFilterFileLoading')
      })
    }
  }
})
