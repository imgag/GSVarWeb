<template>
  <v-app id="inspire">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-title>ngs-remote</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <samples></samples>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Samples from '@/views/Samples'

export default {
  name: 'App',
  components: {
    Samples
  },
  data: () => ({
  })
}
</script>
