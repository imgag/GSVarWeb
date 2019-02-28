/**
 * Parses an item and returns it's header columns
 * @function
 * @param {Array<String>} items
 * @return {Array<Object>}
 */
function produceHeaders (items) {
    return items.map((item) => {
        if (item.startsWith("#")) item = item.substr(1)
        return {
            text: item,
            value: item,
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
        if (line.startsWith("##")) {
            index += 1
        } else {
            break
        }
    }
    return lines.slice(index).map((line) => line.trim().split('\t'))
}

export { produceHeaders, parseTSV }
