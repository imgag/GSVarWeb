<template>
    <v-layout
            justify-center
            align-center
    >
        <v-flex text-xs-center>

            <filter-select :filterNames="filters"></filter-select>
        </v-flex>
    </v-layout>
</template>

<script>
import FilterSelect from '@/components/FilterSelect'
import filterJSON from '@/assets/filters.json'

export default {
    name: "Home.vue",
    data: function () {
        return {
            filters: []
        }
    },
    mounted () {
        this.filters = [].concat(filterJSON.map((filterGroup) => filterGroup)).map((filterGroup) => Object.keys(filterGroup)).flat()
    },
    components: {
        FilterSelect
    }
}
</script>

<style scoped>

</style>