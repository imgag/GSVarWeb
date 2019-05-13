import Vue from 'vue'
import Vuex from 'vuex'

import filterJSON from '@/assets/filters.json'
import { parseTSV, produceHeaders, fileNameFromPath, createFilterConfig, createOAuthProvider } from '@/utils'

const fetchDefaults = require('fetch-defaults')
const flat = require('array.prototype.flat')

Vue.use(Vuex)

const $basePath = (process.env.VUE_APP_BASEPATH) ? process.env.VUE_APP_BASEPATH : 'http://localhost:9000/v1'

let keycloak = createOAuthProvider()

let accessToken = null
if (window.location.hash.startsWith('#state')) {
  try {
    let response = keycloak.parse(window.location.hash)
    accessToken = response.access_token
  } catch (err) {
    console.error(err) // eslint-disable-line no-console
  }
}

const apiFetch = (accessToken === null) ? fetchDefaults(fetch) : fetchDefaults(fetch, {
  headers: {
    authorization: `Bearer ${accessToken}`
  }
})

export default new Vuex.Store({
  state: {
    logged_in: (accessToken !== null),
    filterNames: flat([].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup))),
    lines: [],
    headers: [],

    // Loading states
    filterFileLoading: false,
    fileLoaded: false,
    fileLoading: false,

    // Current file and stage
    lastTotalNumberOfVariants: 0,
    lastSelectedFilterName: '',
    step: 1,

    // Selection
    selectedFilePath: null
  },
  getters: {
  },
  mutations: {
    replaceLines (state, lines) {
      state.lines = lines
    },
    updateHeaders (state, headers) {
      state.headers = produceHeaders(headers)
    },
    toggleFilterFileLoading (state) {
      state.filterFileLoading = !state.filterFileLoading
    },
    toggleFileLoading (state) {
      state.fileLoading = !state.fileLoading
    },
    setFileLoaded (state) {
      state.fileLoaded = true
    },
    updateSelectedFilePath (state, path) {
      state.selectedFilePath = path
    },
    updateLastTotalNumberOfVariants (state, numberOfVariants) {
      state.lastTotalNumberOfVariants = numberOfVariants
    },
    incrementStep (state) {
      state.step = (state.step === 3) ? 2 : state.step + 1
    },
    updateLastSelectedFilterName (state, name) {
      state.lastSelectedFilterName = name
    }
  },
  actions: {
    /**
     * Annotates the current file path
     * @param context
     * @return {Promise<Response>}
     */
    annotateVcf (context) {
      return fetch(`${$basePath}/an_vep/${context.state.selectedFilePath}`).then((response) => response.json())
    },
    /**
     * Converts the current VCF file to a GSvar
     * @param context
     * @return {Promise<Response>}
     */
    convertVcf (context) {
      return fetch(`${$basePath}/vcf2gsvar/${context.state.selectedFilePath}`).then((response) => response.json())
    },
    /**
     * Updates header fields based on first line of a GSVar / VCF
     * @param context
     */
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
    replaceLinesFromString (context, line) {
      let lines = parseTSV(line)
      if (lines[0][0].startsWith('#')) {
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
        xhr.onerror = (err) => { // eslint-disable-line handle-callback-err
          reject(new Error('Could not submit file'))
        }
        xhr.onload = () => {
          if (xhr.status === 200) {
            resolve(xhr.statusText)
          } else {
            reject(xhr.statusText)
          }
        }
        if (accessToken !== null) {
          xhr.setRequestHeader('Authorization', `Bearer ${accessToken}`)
          xhr.withCredentials = true
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
        apiFetch(`${$basePath}/download/${fileName}`, {
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
    updateSelectedFile (context, file) {
      if (context.state.selectedFilePath !== file.value) {
        let vcf = file.value.endsWith('.vcf') // if VCF annotate and/or convert, annotate first
        return Promise.resolve(context.commit('toggleFileLoading'))
          .then(() => context.dispatch('uploadGSVarFile', file))
          .then(() => {
            if (vcf) {
              return context.dispatch('annotateVcf').then(() => {
                return context.dispatch('convertVcf').then((fileName) => Promise.resolve(fileName))
              }).catch((err) => Promise.reject(err))
            } else {
              return Promise.resolve(file.value)
            }
          })
          .then((fileName) => context.dispatch('loadGSVarFileFromPath', fileName))
          .then(() => Promise.resolve(context.commit('updateSelectedFilePath', file.value)))
          .then(() => context.dispatch('updateLastTotalNumberOfVariants'))
          .then(() => Promise.resolve(context.commit('toggleFileLoading')))
          .catch((err) => Promise.reject(err))
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

      return apiFetch(`${$basePath}/VariantFilterAnnotations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          in: fileNameFromPath(context.state.selectedFilePath),
          out: fileNameFromPath(outFile),
          filter: config
        })
      }).then(() => Promise.resolve(context.commit('updateLastSelectedFilterName', name)))
        .then(() => context.dispatch('loadGSVarFileFromPath', outFile))
        .then(() => context.dispatch('loadGSVarFileFromPath', outFile))
        .catch((err) => {
          throw (new Error(err))
        })
    },
    updateLastTotalNumberOfVariants (context) {
      let fileName = fileNameFromPath(context.state.selectedFilePath)
      apiFetch(`${$basePath}/count/${fileName}`).then((response) => {
        if (response.status === 200) {
          return response.json()
            .then((count) => Promise.resolve(context.commit('updateLastTotalNumberOfVariants', Number(count))))
        } else {
          throw (new Error(response.statusText))
        }
      })
    }
  }
})
