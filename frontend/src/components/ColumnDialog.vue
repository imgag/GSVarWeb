<template>
  <v-layout row justify-center>
    <v-dialog
      v-model="dialog"
      max-width="900"
      persistent
    >
      <v-card>
        <v-card-text>
          <v-list class="text-md-center">
            <template v-for="value in Object.entries(item)">
              <v-layout v-bind:key="value[0]">
                <v-flex>
                  <v-subheader>
                    {{ value[0] }}
                  </v-subheader>
                </v-flex>
                <v-flex>
                  <p class="mt-3">{{ value[1] }}</p>
                </v-flex>
              </v-layout>
            </template>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <external-links :selectedGene="item"></external-links>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            flat="flat"
            @click="closeDialog"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import ExternalLinks from '@/components/ExternalLinks'

export default {
  name: 'ColumnDialog',
  components: {
    ExternalLinks
  },
  data () {
    return {
      dialog: true
    }
  },
  methods: {
    closeDialog () {
      this.dialog = false
      this.$emit('close')
    }
  },
  props: {
    item: {
      type: Object
    }
  }
}
</script>

<style scoped>

</style>
