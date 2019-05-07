<template>
  <div>
    <v-input
      type="file"
      hint="Select file"
      persistent-hint
      class="mb-3"
    >
      <input
        type="file"
        @change="selectedFile = $event.target"
        accept=".GSvar,.vcf"
      />
    </v-input>

    <v-btn
      color="primary"
      @click="updateSelectedFile"
      :loading="$store.state.fileLoading"
      :disabled="selectedFile === null"
    >
      Continue
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'FileSelectView',
  data () {
    return {
      selectedFile: null
    }
  },
  methods: {
    updateSelectedFile () {
      if (this.selectedFile) {
        this.$store.dispatch('updateSelectedFile', this.selectedFile)
          .then(() => this.$store.commit('incrementStep'))
      }
    }
  }
}
</script>
