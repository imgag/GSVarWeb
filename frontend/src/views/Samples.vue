<template>
    <v-layout column>
        <v-flex xs2 class="mb-2">
            <filter-select
                    :loading="$store.state.fileLoading"
                    :step="$store.state.step"
                    :filterNames="$store.state.filterNames"
            >
            </filter-select>
        </v-flex>
        <v-flex v-if="$store.state.fileLoaded" xs12>
            <external-links
                    :selectedGenes="$store.state.selectedGenes"
            ></external-links>
            <g-s-var-view
                    :headers="$store.state.headers"
                    :items="$store.state.lines"
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

export default {
    name: "Samples",
    components: {
        FilterSelect,
        GSVarView,
        ExternalLinks
    }
}
</script>

<style scoped>

</style>