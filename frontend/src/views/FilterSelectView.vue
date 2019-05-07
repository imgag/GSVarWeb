<template>
  <div>
    <v-select
      v-model="selectedFilterName"
      :items="$store.state.filterNames"
      label="Select a filter"
    ></v-select>

    <v-btn
      color="primary"
      @click="applyFilter"
      :disabled="(selectedFilterName === $store.state.lastSelectedFilterName) || $store.state.filterFileLoading"
    >
      Apply filter
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'FilterSelectView',
  data () {
    return {
      selectedFilterName: ''
    }
  },
  methods: {
    applyFilter () {
      this.$store.dispatch('applyFilter', this.selectedFilterName)
    }
  }
}
</script>
