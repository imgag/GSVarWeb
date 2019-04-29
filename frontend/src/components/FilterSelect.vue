<template>
    <v-stepper :value="$store.state.step">
        <v-stepper-header>
            <v-stepper-step :complete="$store.state.step > 1" step="1">Log in</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="$store.state.step > 2" step="2">Select GSVar file</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="$store.state.step > 3" step="3">Select filters</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
            <v-stepper-content step="1">
                <v-btn
                        color="primary"
                        @click="login"
                >
                    Login
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="2">
                <v-input
                        type="file"
                        hint="Select file"
                        persistent-hint
                        class="mb-3"
                >
                <input
                        type="file"
                        @change="selectedFile = $event.target"
                        accept=".GSvar"
                />
                </v-input>

                <v-btn
                        color="primary"
                        @click="updateSelectedFile"
                        :loading="loading"
                        :disabled="selectedFile === null"
                >
                    Continue
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="3">
                <v-select
                        v-model="selectedFilterName"
                        :items="filterNames"
                        hint="Select filter"
                        persistent-hint
                        class="mb-3"
                ></v-select>

                <v-btn
                        color="primary"
                        @click="applyFilter"
                        :disabled="(selectedFilterName === $store.state.lastSelectedFilterName) || $store.state.filterFileLoading"
                >
                    Apply filter
                </v-btn>

                <v-btn flat @click="$store.commit('incrementStep')">Select file</v-btn>
            </v-stepper-content>
        </v-stepper-items>
    </v-stepper>
</template>

<script>
import { createOAuthProvider } from '@/utils'
const OAuth = require('@zalando/oauth2-client-js')

export default {
  name: 'FilterSelect',
  data: function () {
    return {
      selectedFile: null,
      selectedFilterName: '',
      keycloak: null
    }
  },
  mounted () {
    if (this.$store.state.logged_in && this.$store.state.step < 2) {
      this.$store.commit('incrementStep')
    }
  },
  methods: {
    login () {
      let keycloak = createOAuthProvider()

      let request = new OAuth.Request({
        client_id: 'account',
        redirect_uri: location.origin
      })

      let uri = keycloak.requestToken(request)
      keycloak.remember(request)

      window.location.href = uri // redirect to OAuth provider
    },
    updateSelectedFile () {
      if (this.selectedFile) {
        this.$store.dispatch('updateSelectedFile', this.selectedFile)
          .then(() => this.$store.commit('incrementStep'))
      }
    },
    applyFilter () {
      this.$store.dispatch('applyFilter', this.selectedFilterName)
    }
  },
  props: {
    loading: {
      type: Boolean,
      required: true
    },
    step: {
      type: Number,
      required: true
    },
    filterNames: {
      type: Array,
      required: true
    }
  }
}
</script>
