<template>
  <v-layout>
    <v-flex xs10>
      <v-select
        v-model="selectedFilterName"
        :items="$store.state.filterNames"
        label="Select a filter"
        :disabled="$store.state.filterFileLoading"
        @change="updateSelectedFilter"
        clearable
      ></v-select>
    </v-flex>

    <v-flex>
      <v-btn
        @click="$store.commit('incrementStep')"
        class="ml-3"
      >
        Select file
      </v-btn>
    </v-flex>

    <v-flex>
      <v-btn
        @click="$store.dispatch('downloadFile')"
      >
        Download file
      </v-btn>
    </v-flex>

    <v-flex>
      <v-btn
        :href="LOGOUT_URL"
      >
        Logout
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import { LOGOUT_URL } from '@/utils'

export default {
  name: 'FilterSelectView',
  data () {
    return {
      selectedFilterName: '',
      LOGOUT_URL: LOGOUT_URL
    }
  },
  methods: {
    updateSelectedFilter () {
      let vm = this
      vm.$store.dispatch('applyFilter', vm.selectedFilterName)
        .then(() => {
          vm.$store.commit('toggleFilterFileLoading')
        }).catch((err) => {
          vm.$store.commit('toggleFilterFileLoading')
          err.then((body) => {
            vm.$emit('error', body.detail)
          })
        })
    }
  }
}
</script>
