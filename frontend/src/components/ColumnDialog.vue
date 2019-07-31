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
              <v-flex xs-12>
                <v-data-table
                  max-width
                  :rows-per-page-items="codingSplicingRowsPerPage"
                  :headers="codingSplicingHeaders"
                  :items="parseCodingSplicingInfo(item.coding_and_splicing)"
                >
                  <template v-slot:items="props">
                    <td><a :href="`https://gnomad.broadinstitute.org/gene/${props.item.Gene}`" target="_blank">{{ props.item.Gene }}</a></td>
                    <td><a :href="`http://grch37.ensembl.org/Homo_sapiens/Transcript/Summary?t=${props.item.Transcript}`" target="_blank">{{ props.item.Transcript }}</a></td>
                    <td>{{ props.item.Impact }}</td>
                    <td>{{ props.item.Type }}</td>
                    <td>{{ props.item.Exon.replace(/^(exon)/, '') }}</td>
                    <td>{{ props.item.cDNA }}</td>
                    <td>{{ props.item.Protein }}</td>
                    <td v-if="props.item.Domain"><a :href="`https://pfam.xfam.org/family/${props.item.Domain}`" target="_blank">{{ props.item.Domain }}</a></td>
                    <td v-else></td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
            <v-flex>
              <v-divider class="mb-3"></v-divider>
            </v-flex>
            <v-layout>
              <v-flex>
                <p class="title">Splicing</p>
                <p>MaxEntScan: {{ item.MaxEntScan }}</p>
                <p v-if="item.GeneSplicer">GeneSplicer:<br/>
                  <span v-for="splicer in item.GeneSplicer.split('&')" v-bind:key="splicer">
                    {{ splicer }}<br/>
                  </span>
                </p>
                <p>dbscSNV: {{ item.dbscSNV }}</p>
                <p class="title">Regulatory</p>
                <p>Regulatory: {{ item.regulatory.replace('regulatory_region_variant:', '') }}</p>
              </v-flex>
              <v-flex>
                <p class="title">Databases</p>
                <p>dbSNP: <a :href="`https://www.ncbi.nlm.nih.gov/snp/${item.dbSNP}`" v-if="item.dbSNP" target="_blank">{{ item.dbSNP }}</a></p>
                <p>ClinVar:
                  <a :href="`https://www.ncbi.nlm.nih.gov/clinvar/variation/${getID(item.ClinVar)}`" v-if="item.ClinVar" target="_blank">
                    <span :title="item.ClinVar" data-toggle="tooltip" v-bind:style="colors('ClinVar')">{{ getID(item.ClinVar) }}</span>
                  </a>
                </p>
                <p>HGMD:
                  <a :href="`https://portal.biobase-international.com/hgmd/pro/mut.php?acc=${getID(item.HGMD)}`" target="_blank">
                    <span :title="item.HGMD" data-toggle="tooltip" v-bind:style="colors('HGMD')">{{ getID(item.HGMD) }}</span>
                  </a>
                </p>
                <p>OMIM:
                  <a :href="`https://omim.org/entry/${getID(item.OMIM)}`" v-if="item.OMIM" target="_blank">
                    <span :title="item.OMIM" data-toggle="tooltip">{{ getID(item.OMIM) }}</span>
                  </a>
                </p>
                <p v-if="item.COSMIC">COSMIC:
                  <span v-for="COSMIC in item.COSMIC.split(',')" v-bind:key="COSMIC">
                    <a :href="`https://cancer.sanger.ac.uk/cosmic/search?q=${COSMIC}`" target="_blank">{{ COSMIC }}</a>&nbsp;
                  </span>
                </p>
              </v-flex>
              <v-flex>
                <p class="title">Frequencies</p>
                <p>1000g: {{ item['1000g'] }}</p>
                <p>gnomAD: <a :href="`https://gnomad.broadinstitute.org/variant/${item.chr}-${item.start}-${item.ref}-${item.obs}`" target="_blank">{{ item.gnomAD }}</a></p>
                <p>gnomAD (hom/hem): {{ item.gnomAD_hom_hemi }}</p>
                <p>gnomAD (sub): {{ item.gnomAD_sub }}</p>
                <p>ESP (sub): {{ item.ESP }}</p>
              </v-flex>
              <v-flex>
                <p class="title">Pathogenicity</p>
                <p>phyloP: {{ item.phyloP }}</p>
                <p>Sift: {{ item.Sift }}</p>
                <p>PolyPhen: {{ item.PolyPhen }} </p>
                <p>fathmm-MKL:  {{ item['fathmm-MKL'] }}</p>
                <p>CADD: {{ item.CADD }}</p>
                <p>REVEL: {{ item.REVEL }}</p>
              </v-flex>
              <v-flex>
                <p class="title">Classification</p>
                <div v-if="item.classification !== undefined && item.classification !== '.'">
                  <p class="subheading mt-1">Previous classifications</p>
                  <p v-for="classification in item.classification.split(',')" :key="classification">{{ formatClassification(classification) }}</p>
                </div>
                <p class="subheading mt-auto">Classificate yourself</p>
                <v-select :items="classifications" @input="classificate" outline></v-select>
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
      classifications: [
        'benign',
        'likely benign',
        'variant of unknown significance',
        'likely pathogenic',
        'pathogenic'
      ],
      dialog: true,
      codingSplicingRowsPerPage: [15, 25, { 'text': '$vuetify.dataIterator.rowsPerPageAll', 'value': -1 }],
      codingSplicingHeaders: [
        { text: 'Gene', sortable: false },
        { text: 'Transcript', sortable: false },
        { text: 'Impact', sortable: false },
        { text: 'Type', sortable: false },
        { text: 'Exon', sortable: false },
        { text: 'cDNA', sortable: false },
        { text: 'Protein', sortable: false },
        { text: 'Domain', sortable: false }
      ]
    }
  },
  methods: {
    classificate (classification) {
      this.$store.dispatch('updateRating', {
        rating: this.classifications.indexOf(classification) + 1,
        chr: this.item.chr,
        start: this.item.start,
        end: this.item.end
      }).then(() => {
        this.$store.dispatch('loadGSvarFileFromPath', this.$store.state.selectedFilePath)
      }).catch((err) => console.error(err)) // eslint-disable-line no-console
    },
    formatClassification (classification) {
      let components = classification.split(':')
      classification = this.classifications[parseInt(components[1] - 1)]
      return `${components[0]} rated this variant with ${classification}`
    },
    colors (property) {
      if (property === 'HGMD') {
        return (this.item.HGMD.includes('CLASS=DM')) ? 'background-color: red;' : ''
      }
      if (property === 'ClinVar') {
        if (this.item.ClinVar.includes('pathogenic') && !this.item.ClinVar.includes('conflicting interpretations of pathogenicity')) {
          return 'background-color: red;'
        } else if (this.item.ClinVar.includes('(confirmed)')) {
          return 'background-color: yellow;'
        }
        return ''
      }
    },
    parseCodingSplicingInfo (text) {
      return text.split(',').map((e) => e.split(':')).map((item) => {
        return {
          Gene: item[0],
          Transcript: item[1],
          Impact: item[3],
          Type: item[2],
          Exon: item[4],
          cDNA: item[5],
          Protein: item[6],
          Domain: item[7]
        }
      })
    },
    getID (text) {
      return text.substring(0, text.indexOf('[')).trim()
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
