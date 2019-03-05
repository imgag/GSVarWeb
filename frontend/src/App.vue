<template>
  <v-app id="inspire">
    <v-toolbar color="indigo" dark fixed app>
      <v-toolbar-title>ngs-bits</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <samples></samples>
      </v-container>
    </v-content>
    <v-footer color="indigo" app>
      <span class="white--text ml-2">Institute of Medical Genetics and Applied Genomics &copy; 2019</span>
    </v-footer>
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
