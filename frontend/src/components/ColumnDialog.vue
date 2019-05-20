<template>
  <v-layout row justify-center>
    <v-dialog
      v-model="dialog"
      max-width="900"
      persistent
    >
      <v-card>
        <v-card-text>
          <v-layout row>
            <v-flex xs-4>
              <p>Chromosome: {{ item.chr }}</p>
              <p>Start: {{ item.start }}</p>
              <p>End: {{ item.end }}</p>
              <p>Reference: {{ item.ref }}</p>
              <p>Observed: {{ item.obs }}</p>
              <p v-if="item.gene">Gene: {{ item.gene }}</p>
            </v-flex>
            <v-flex xs-4>
              <p v-if="item.phyloP">phyloP: {{ item.phyloP }}</p>
              <p v-if="item.Sift">Sift: {{ item.Sift }}</p>
              <p v-if="item.PolyPhen">PolyPhen: {{ item.PolyPhen }} </p>
              <p v-if="item.fathmm">fathmm-MKL:  {{ item.fathmm }}</p>
              <p v-if="item.CADD">CADD: {{ item.CADD }}</p>
              <p v-if="item.REVEL">REVEL: {{ item.REVEL }}</p>
              <p v-if="item.MaxEntScan">MaxEntScan: {{ item.MaxEntScan }}</p>
              <p v-if="item.GenSplicer">GenSplicer: {{ item.GenSplicer }}</p>
            </v-flex>
            <v-flex xs-4 v-if="item.OMIM || item.classification">
              <p v-if="item.OMIM">OMIM: {{ item.OMIM }}</p>
              <div v-if="item.classification" xs-2>
                <p>Classification: {{ item.classification }}</p>
                <p v-if="item.classification_comment" class="text-muted">Comment: {{ item.classification_comment }}</p>
              </div>
            </v-flex>
          </v-layout>
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
p {
word-break: break-all;
}
</style>
