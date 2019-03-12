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
    headers: [],

    // Loading states
    filterFileLoading: false,
    fileLoaded: false,
    fileLoading: false,

    // Current file and stage
    lastTotalNumberOfVariants: 0,
    step: 1,

    // Selection
    selectedGenes: [],
    selectedFilePath: null
  },
  getters: {
  },
  mutations: {
    replaceLines(state, lines) {
      state.lines = lines
    },
    updateHeaders(state, headers) {
      state.headers = produceHeaders(headers)
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
    updateSelectedFilePath(state, path) {
      state.selectedFilePath = path
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
    updateHeaders (context) {
      let lines = context.state.lines
      let header = lines.splice(0, 1)
      context.commit('replaceLines', lines)
      context.commit('updateHeaders', header[0])
    },
    /**
     * Parses lines
     * @function
     * @param context
     * @param line
     */
    replaceLinesFromString(context, line) {
      let lines = parseTSV(line)
      if (lines[0][0].startsWith("#")) {
        let header = lines.splice(0, 1)
        context.commit('updateHeaders', header[0])
      }
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
        fetch(`${$basePath}/download/${fileName}`, {
          headers: {
            'Lines': '1-500'
          }
        }).then((response) => {
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
     * Updates selected file
     * @function
     * @param context
     * @param file
     */
    updateSelectedFile(context, file) {
      if (context.state.selectedFilePath !== file.value) {
        context.commit('toggleFileLoading')
        context.dispatch('uploadGSVarFile', file).then(() => {
          context.dispatch('loadGSVarFileFromPath', file.value).then(() => {
            context.commit('updateSelectedFilePath', file.value)
            context.dispatch('updateLastTotalNumberOfVariants')
            context.commit('toggleFileLoading')
            context.commit('incrementStep')
          })
        })
      } else {
        context.commit('incrementStep')
      }
    },
    /**
     * Applies filter with new file path
     * @function
     * @param context
     * @param name
     */
    applyFilter (context, name) {
      let config = createFilterConfig(filterJSON, name)
      let dateAppend = String(Date.now())
      let outFile = context.state.selectedFilePath.replace('.GSvar', `_${dateAppend}.GSVar`)
      context.commit('toggleFilterFileLoading')

      fetch(`${$basePath}/VariantFilterAnnotations`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          in: fileNameFromPath(context.state.selectedFilePath),
          out: fileNameFromPath(outFile),
          filter: config
        })
      }).then(() => {
        context.dispatch('loadGSVarFileFromPath', outFile)
        context.commit('toggleFilterFileLoading')
      }).catch((err) => {
        console.error(err) // eslint-disable-line no-console
        context.commit('toggleFilterFileLoading')
      })
    },
    updateLastTotalNumberOfVariants(context) {
      let fileName = fileNameFromPath(context.state.selectedFilePath)
      fetch(`${$basePath}/count/${fileName}`).then((response) => {
        if (response.status === 200) {
          response.json().then((count) => {
            context.commit('updateLastTotalNumberOfVariants', count)
          })
        } else {
          console.error(response.statusText) // eslint-disable-line no-console
        }
      })
    }
  }
})
