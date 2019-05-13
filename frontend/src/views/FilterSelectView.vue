<template>
  <v-layout>
    <v-flex xs10>
      <v-select
        v-model="selectedFilterName"
        :items="$store.state.filterNames"
        label="Select a filter"
      ></v-select>
    </v-flex>

    <v-flex>
      <v-btn
        color="primary"
        @click="$store.dispatch('applyFilter', selectedFilterName)"
        :disabled="(selectedFilterName === $store.state.lastSelectedFilterName) || $store.state.filterFileLoading"
      >
        Apply filter
      </v-btn>
    </v-flex>

    <v-flex>
      <v-btn
        @click="$store.commit('incrementStep')"
      >
        Select file
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'FilterSelectView',
  data () {
    return {
      selectedFilterName: ''
    }
  }
}
</script>
