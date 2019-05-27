<template>
  <v-layout row justify-center>
    <v-dialog
      v-model="dialog"
      full-width
      @keydown.esc="dialog = false"
    >
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          {{ item.chr }}:{{ item.start }}-{{ item.end }} {{ item.ref }} > {{ item.obs }}
        </v-card-title>
        <v-card-title
          class="grey lighten-2"
        >
          Gene(s): {{ item.gene }}
        </v-card-title>
        <v-card-text>
          <v-layout column>
            <v-layout row>
              <v-flex v-for="prop in parseCodingSplicingInfo(item.coding_and_splicing)" :key="prop.ID">
                <p class="subheading"><a :href="`http://exac.broadinstitute.org/gene/${prop.Gene}`" target="_blank">{{ prop.Gene }}</a> (<a :href="`http://grch37.ensembl.org/Homo_sapiens/Transcript/Summary?t=${prop.ID}`" target="_blank">{{ prop.ID }}</a>)</p>
                <p>Type: {{ prop.Type }}</p>
                <p>Impact: {{ prop.Impact }}</p>
                <p>Exon: {{ prop.Exon }}</p>
                <p>cDNA: {{ prop.cDNA }}</p>
                <p>Protein: {{ prop.Protein }}</p>
                <p>Domain: {{ prop.Domain }}</p>
              </v-flex>
            </v-layout>
            <v-flex>
              <v-divider class="mb-3"></v-divider>
            </v-flex>
            <v-layout>
              <v-flex>
                <p class="subheading">Splicing</p>
                <p>MaxEntScan: {{ item.MaxEntScan }}</p>
                <p>GeneSplicer: {{ item.GeneSplicer }}</p>
                <p>dbscSNV: {{ item.dbscSNV }}</p>
                <p class="subheading">Regulatory</p>
                <p>Regulatory: {{ item.regulatory }}</p>
              </v-flex>
              <v-flex>
                <p class="subheading">Databases</p>
                <p>dbSNP: <a :href="`https://www.ncbi.nlm.nih.gov/snp/${item.dbSNP}`" v-if="item.dbSNP" target="_blank">{{ item.dbSNP }}</a></p>
                <p>ClinVar: <a :href="`https://www.ncbi.nlm.nih.gov/clinvar/variation/${getID(item.ClinVar)}`" v-if="item.ClinVar" target="_blank">{{ getID(item.ClinVar) }}</a></p>
                <p>HGMD: {{ item.HGMD }}</p>
                <p>OMIM: <a :href="`https://omim.org/entry/${getID(item.OMIM)}`" v-if="item.OMIM" target="_blank">{{ getID(item.OMIM) }}</a></p>
                <p>COSMIC: <a :href="`https://cancer.sanger.ac.uk/cosmic/search?q=${item.COSMIC}`" v-if="item.COSMIC" target="_blank">{{ item.COSMIC }}</a></p>
              </v-flex>
              <v-flex>
                <p class="subheading">Frequencies</p>
                <p>1000g: {{ item['1000g'] }}</p>
                <p>gnomAD: {{ item.gnomAD }}</p>
                <p>gnomAD (hom/hem): {{ item.gnomAD_hom_hemi }}</p>
                <p>gnomAD (sub): {{ item.gnomAD_sub }}</p>
                <p>ESP (sub): {{ item.ESP }}</p>
              </v-flex>
              <v-flex>
                <p class="subheading">Pathogenicity</p>
                <p>phyloP: {{ item.phyloP }}</p>
                <p>Sift: {{ item.Sift }}</p>
                <p>PolyPhen: {{ item.PolyPhen }} </p>
                <p>fathmm-MKL:  {{ item['fathmm-MKL'] }}</p>
                <p>CADD: {{ item.CADD }}</p>
                <p>REVEL: {{ item.REVEL }}</p>
              </v-flex>
            </v-layout>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <external-links :selectedGene="item"></external-links>
          <v-btn
            color="green darken-1"
            flat="flat"
            @click="dialog = false"
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
    parseCodingSplicingInfo (text) {
      return text.split(',').map((e) => e.split(':')).map((item) => {
        return {
          Gene: item[0],
          ID: item[1],
          Type: item[3],
          Impact: item[4],
          Exon: item[5],
          cDNA: item[6],
          Protein: item[7],
          Domain: item[8]
        }
      })
    },
    getID (text) {
      return text.substring(0, text.indexOf('[') - 2)
    }
  },
  watch: {
    dialog () {
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
