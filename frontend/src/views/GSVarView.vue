<template>
    <v-data-table
        :headers="headers"
        :items="items"
        class="elevation-1"
        :rows-per-page-items="rowsPerPage"
        :loading="loading"
    >
        <template slot="headers" slot-scope="props">
            <tr>
                <th></th> <!-- insert empty th for selectable behaviour -->
                <th
                    v-for="header in props.headers"
                    :key="header.text"
                >
                    {{ header.text }}
                </th>
            </tr>
        </template>
        <template slot="items" slot-scope="props">
            <td>
                <v-checkbox
                    primary
                    @change="updateSelectedGenes(props.item, $event)"
                    hide-details
                ></v-checkbox>
            </td>
            <td v-for="(item, index) in props.item" v-bind:key="index" :bgcolor="getColor(item, index)">
                <tooltip-text :text="item"></tooltip-text>
            </td>
        </template>

        <template slot="actions-append">
            <p class="mt-3 mr-3">Original variants: {{ lastTotalNumberOfVariants }}</p>
        </template>

    </v-data-table>
</template>

<script>
import TooltipText from '@/components/TooltipText'

/// NOTE: Since the headers are sorted this array also needs to be sorted by index
const columnHeaders = ['chr', 'start', 'end', 'ref', 'obs', 'gene', 'coding_and_splicing', 'ClinVar', 'HGMD', 'NGSD_hom', 'NGSD_het', 'classification', 'validation', 'comment']

export default {
  name: 'GSVarView',
  components: {
    TooltipText
  },
  data: function () {
    return {
      selectedGenes: [],
      rowsPerPage: [
        15,
        30,
        50,
        100
      ]
    }
  },
  computed: {
    colorIndexes () {
      let headers = this.$store.state.headers.map((header) => header.value)
      return headers.filter((header) => columnHeaders.includes(header)).map((header) => headers.indexOf(header))
    },
    columnMap () {
      return this.colorIndexes.reduce((result, item, index) => {
        result[columnHeaders[index]] = item
        return result
      }, {})
    }
  },
  methods: {
    /**
         * Adds a gene to the list of selected genes if selected is true.
         * Otherwise tries to remove this gene from the list
         * @function
         * @param column
         * @param selected
         */
    updateSelectedGenes (column, selected) {
      let selectedGene = {
        chr: column[this.columnMap['chr']],
        start: column[this.columnMap['start']],
        end: column[this.columnMap['end']],
        ref: column[this.columnMap['ref']],
        obs: column[this.columnMap['obs']],
        gene: column[this.columnMap['gene']]
      }

      if (selected) {
        this.selectedGenes.push(selectedGene)
        this.$store.commit('updateSelectedGenes', this.selectedGenes)
      } else {
        let geneIndex = this.selectedGenes.findIndex((item) => item.start === selectedGene.start)
        if (geneIndex > -1) {
          this.selectedGenes.splice(geneIndex, 1)
          this.$store.commit('updateSelectedGenes', this.selectedGenes)
        }
      }
    },
    /// Ported from https://github.com/imgag/ngs-bits/blob/master/src/GSvar/VariantTable.cpp#L114
    getColor (item, index) {
      let color = ''

      // warning
      if (index === this.columnMap['coding_and_splicing'] && item.includes(':HIGH:')) {
        color = 'red'
      }

      if (index === this.columnMap['classification'] && (item === '3' || item === 'M')) {
        color = 'orange'
      } else if (index === this.columnMap['classification'] && (item === '4' || item === '5')) {
        color = 'red'
      } else if (index === this.columnMap['classification'] && item.includes('pathogenic')) {
        color = 'red'
      } else if (index === this.columnMap['classification'] && item.includes('CLASS=DM')) {
        color = 'red'
      }

      if (index === this.columnMap['classification'] && (item === '0' || item === '1' || item === '2')) { // non-pathogenic
        color = 'green'
      }

      // highlighted
      if (index === this.columnMap['validation'] && item.includes('TP')) {
        color = 'yellow'
      } else if (index === this.columnMap['comment'] && item !== '') {
        color = 'yellow'
      } else if (index === this.columnMap['NGSD_hom'] && item === '0') {
        color = 'yellow'
      } else if (index === this.columnMap['NGSD_het'] && item === '1') {
        color = 'yellow'
      } else if (index === this.columnMap['ClinVar'] && item.includes('confirmed')) {
        color = 'yellow'
      } // else if (index === this.columnMap["genes"]) /// TODO: Deal with imprinting genes

      return color
    }
  },
  props: {
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    },
    lastTotalNumberOfVariants: {
      type: Number,
      default: 0
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
td {
    max-width: 100ch;
    word-wrap:break-word
}
</style>
