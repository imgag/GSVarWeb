<template>
  <v-app id="inspire">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-title>GSvarWeb</v-toolbar-title>
    </v-toolbar>
    <!-- used for error reporting -->
    <v-snackbar
      v-model="snackbar"
      top
    >
      {{ text }}
      <v-btn
        color="pink"
        flat
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>
    <!-- main navigation -->
    <v-content>
      <v-container fluid fill-height>
        <v-layout column>
          <v-flex xs1 class="mb-2" v-if="$store.state.step === 2">
            <file-select-view @error="showError"></file-select-view>
          </v-flex>
          <v-flex xs1 class="mb-2" v-if="$store.state.step === 3">
            <filter-select-view @error="showError"></filter-select-view>
          </v-flex>
          <v-flex v-if="$store.state.fileLoaded" xs10>
            <GSvarView
              :headers="$store.state.headers"
              :items="$store.state.lines"
              :loading="$store.state.filterFileLoading"
              :lastTotalNumberOfVariants="$store.state.lastTotalNumberOfVariants"
            />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import GSvarView from '@/views/GSvarView'
import FileSelectView from '@/views/FileSelectView'
import FilterSelectView from '@/views/FilterSelectView'
import { createOAuthProvider } from '@/utils'

const OAuth = require('@zalando/oauth2-client-js')

export default {
  name: 'App',
  data () {
    return {
      snackbar: false,
      text: ''
    }
  },
  mounted () {
    if (!this.$store.state.logged_in) {
      this.login()
    } else if (this.$store.state.logged_in && this.$store.state.step < 2) {
      this.$store.commit('incrementStep')
    }
  },
  methods: {
    showError (text) {
      this.text = text
      this.snackbar = true
    },
    login () {
      let keycloak = createOAuthProvider()
      let request = new OAuth.Request({
        client_id: 'account',
        redirect_uri: location.origin
      })
      let uri = keycloak.requestToken(request)
      keycloak.remember(request)
      window.location.href = uri // redirect to OAuth provider
    }
  },
  components: {
    FilterSelectView,
    FileSelectView,
    GSvarView
  }
}
</script>
