<template>
  <v-app id="inspire">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-title>ngs-remote</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout column>
          <v-flex xs2 class="mb-2" v-if="$store.state.step === 2">
            <file-select-view></file-select-view>
          </v-flex>
          <v-flex xs class="mb-2" v-if="$store.state.step === 3">
            <filter-select-view></filter-select-view>
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
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import GSVarView from '@/views/GSVarView'
import FileSelectView from '@/views/FileSelectView'
import FilterSelectView from '@/views/FilterSelectView'
import { createOAuthProvider } from '@/utils'

const OAuth = require('@zalando/oauth2-client-js')

export default {
  name: 'App',
  mounted () {
    if (!this.$store.state.logged_in) {
      this.login()
    } else if (this.$store.state.logged_in && this.$store.state.step < 2) {
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
    }
  },
  components: {
    FilterSelectView,
    FileSelectView,
    GSVarView
  }
}
</script>
