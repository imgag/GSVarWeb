<template>
    <v-layout column>
        <v-flex xs2 class="mb-2">
            <filter-select :filterNames="filters" v-on:updateSelectedFile="loadGSVarFileFromPath($event)"></filter-select>
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
import { parseTSV } from '@/utils'

const addr = 'http://localhost:9000/v1'

export default {
    name: "Home",
    data: function () {
        return {
            filters: [],
            loaded: false,
            lines: []
        }
    },
    mounted () {
        this.filters = [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat()
    },
    methods: {
      loadGSVarFileFromPath (path) {
          let vm = this
          let fileName = path.replace(/^.*[\\\/]/, '')
          fetch(`${addr}/download/${fileName}`).then((response) => {
              if (response.status === 200) {
                  response.text().then((lines) => {
                      vm.lines = parseTSV(lines)
                      vm.loaded = true
                  })
              }
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