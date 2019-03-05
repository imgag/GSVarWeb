<template>
    <v-layout column>
        <v-flex xs2 class="mb-2">
            <filter-select
                    :filterNames="filters"
                    v-on:updateSelectedFile="updateSelectedFile($event)"
                    v-on:applyFilter="applyFilter($event)"
            >
            </filter-select>
        </v-flex>
        <v-flex v-if="loaded" xs12>
            <g-s-var-view :lines="lines"></g-s-var-view>
        </v-flex>
    </v-layout>
</template>

<script>
import FilterSelect from '@/components/FilterSelect'
import GSVarView from '@/components/GSVarView'
import filterJSON from '@/assets/filters.json'
import { parseTSV, createFilterConfig } from '@/utils'

export default {
    name: "Home",
    data: function () {
        return {
            filters: [],
            loaded: false,
            lines: [],
            lastPath: null
        }
    },
    mounted () {
        this.filters = [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat()
    },
    methods: {
        fileNameFromPath(path) {
          return path.replace(/^.*[\\\/]/, '') // eslint-disable-line
        },
        loadGSVarFileFromPath (path) {
            let vm = this
            return new Promise((resolve, reject) => {
                let fileName = vm.fileNameFromPath(path)
                fetch(`${vm.$basePath}/download/${fileName}`).then((response) => {
                    if (response.status === 200) {
                        response.text().then((lines) => {
                            vm.lines = parseTSV(lines)
                            vm.loaded = true
                            resolve(response.statusText)
                        })
                    } else {
                        reject(response.statusText)
                    }
                })
            })
        },
        uploadGSVarFile (file) {
            let vm = this
            return new Promise((resolve, reject) => {
                let formData = new FormData()
                formData.append('uploadedFile', file.files[0])
                let xhr = new XMLHttpRequest()
                xhr.open('POST', `${vm.$basePath}/upload`, true)
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
        updateSelectedFile (file) {
            let vm = this
            if (vm.lastPath !== file.value) {
                vm.uploadGSVarFile(file).then(() => {
                    vm.loadGSVarFileFromPath(file.value).then(() => {
                        vm.lastPath = file.value
                    })
                })
            }
        },
        applyFilter (name) {
            let vm = this
            let config = createFilterConfig(filterJSON, name)
            let dateAppend = String(Date.now())
            let outFile = vm.lastPath.replace('.GSvar', `_${dateAppend}.GSVar`)

            fetch(`${vm.$basePath}/VariantFilterAnnotations`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    in: vm.fileNameFromPath(vm.lastPath),
                    out: vm.fileNameFromPath(outFile),
                    filter: config
                })
            }).then(() => {
                vm.loadGSVarFileFromPath(outFile)
            })
        }
    },
    components: {
        FilterSelect,
        GSVarView
    }
}
</script>

<style scoped>

</style>