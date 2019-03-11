<template>
    <v-layout column>
        <v-flex xs2 class="mb-2">
            <filter-select
                    :filterNames="$store.state.filterNames"
                    v-on:updateSelectedFile="updateSelectedFile($event)"
                    v-on:applyFilter="applyFilter($event)"
            >
            </filter-select>
        </v-flex>
        <v-flex v-if="$store.state.fileLoaded" xs12>
            <external-links
                    :selectedGenes="$store.state.selectedGenes"
            ></external-links>
            <g-s-var-view
                    :headers="$store.getters.headers"
                    :items="$store.getters.items"
                    :loading="$store.state.filterFileLoading"
                    :lastTotalNumberOfVariants="$store.state.lastTotalNumberOfVariants"
            >
            </g-s-var-view>
        </v-flex>
    </v-layout>
</template>

<script>
import FilterSelect from '@/components/FilterSelect'
import GSVarView from '@/components/GSVarView'
import ExternalLinks from '@/components/ExternalLinks'
import { createFilterConfig, fileNameFromPath } from '@/utils'
import filterJSON from '@/assets/filters.json'

export default {
    name: "Samples",
    methods: {
        loadGSVarFileFromPath (path) {
            let vm = this
            return new Promise((resolve, reject) => {
                let fileName = fileNameFromPath(path)
                fetch(`${vm.$basePath}/download/truncated/${fileName}`).then((response) => {
                    if (response.status === 200) {
                        response.text().then((line) => {
                            vm.$store.dispatch('replaceLinesFromString', line)
                            vm.$store.commit('setFileLoaded')
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
            if (vm.$store.state.lastPath !== file.value) {
                vm.uploadGSVarFile(file).then(() => {
                    vm.loadGSVarFileFromPath(file.value).then(() => {
                        vm.$store.commit('updateLastPath', file.value)
                        vm.$store.commit('updateLastTotalNumberOfVariants', vm.$store.state.lines.length)
                    })
                })
            }
        },
        applyFilter (name) {
            let vm = this
            let config = createFilterConfig(filterJSON, name)
            let dateAppend = String(Date.now())
            let outFile = vm.$store.state.lastPath.replace('.GSvar', `_${dateAppend}.GSVar`)
            vm.$store.commit('toggleFilterFileLoading')

            fetch(`${vm.$basePath}/VariantFilterAnnotations`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    in: fileNameFromPath(vm.$store.state.lastPath),
                    out: fileNameFromPath(outFile),
                    filter: config
                })
            }).then(() => {
                vm.loadGSVarFileFromPath(outFile)
                vm.$store.commit('toggleFilterFileLoading')
            }).catch((err) => {
                console.error(err) // eslint-disable-line
                vm.$store.commit('toggleFilterFileLoading')
            })
        }
    },
    components: {
        FilterSelect,
        GSVarView,
        ExternalLinks
    }
}
</script>

<style scoped>

</style>