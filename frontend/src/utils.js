const OAuth = require('@zalando/oauth2-client-js')
const REALM = (process.env.VUE_APP_REALM !== undefined) ? process.env.VUE_APP_REALM : 'debug'
const AUTHORIZATION_URL = `https://auth.imgag.de/auth/realms/${REALM}/protocol/openid-connect/auth`

/**
 * Creates an OAuth provider for keycloak
 * @function
 * @return {OAuth.Provider}
 */
function createOAuthProvider () {
  return new OAuth.Provider({
    id: 'keycloak',
    authorization_url: AUTHORIZATION_URL
  })
}

/**
 * Parses an item and returns it's header columns
 * @function
 * @param {Array<String>} items
 * @return {Array<Object>}
 */
function produceHeaders (items) {
  return items.map((item) => {
    if (item.startsWith('#')) item = item.substr(1)
    return {
      headerName: item,
      field: item,
      sortable: false
    }
  })
}

/**
 * Parses a string and returns it's items (expects TSV format)
 * @function
 * @param lines
 * @return {Array<Array<String>>}
 */
function parseTSV (lines) {
  lines = lines.split('\n')
  let index = 0
  for (let line of lines) {
    if (line.startsWith('##')) {
      index += 1
    } else {
      break
    }
  }
  return lines.slice(index).filter((l) => l.length > 0).map((line) => line.trim().split('\t'))
}

/**
 * Returns the filter config for the specified filter
 * @function
 * @param {Array<Object>} filterConfig
 * @param {String} name
 * @return {Array<Object>}
 */
function createFilterConfig (filterConfig, name) {
  // NOTE: Only one key is supported at a time currently
  return filterConfig.map((filterGroup) => {
    let matches = Object.keys(filterGroup).filter((filter) => filter === name)
    let obj = {}
    if (matches.length) obj[name] = filterGroup[name]
    return obj
  }).filter((filterGroup) => Object.keys(filterGroup).length)
}

/**
 * Returns the file name for a given path
 * @function
 * @param path
 * @return {*}
 */
function fileNameFromPath (path) {
    return path.replace(/^.*[\\\/]/, '') // eslint-disable-line
}

export { createFilterConfig, createOAuthProvider, fileNameFromPath, parseTSV, produceHeaders }
