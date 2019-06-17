<template>
  <div>
    <column-dialog v-if="shouldOpen" @close="closeDialog" :item="columnItem"></column-dialog>
    <v-data-table
      :headers="headers"
      :items="items"
      :rows-per-page-items="rowsPerPage"
      :loading="loading"
    >
      <template slot="headers" slot-scope="props">
        <tr>
          <th
            v-for="header in props.headers"
            :key="header.text"
          >
            {{ header.text }}
          </th>
        </tr>
      </template>
      <template slot="items" slot-scope="props">
        <td v-for="(item, index) in props.item" v-bind:key="index" :bgcolor="getColor(item, index)" v-on:click="openColumnDialog(props.item)">
          <tooltip-text :text="item" v-if="index === columnMap['gene']"></tooltip-text>
          <tooltip-text :text="item" v-else-if="index === columnMap['coding_and_splicing']"></tooltip-text>
          <tooltip-text :text="item" v-else-if="index === columnMap['regulatory']"></tooltip-text>
          <tooltip-text :text="item" :limit=50 v-else-if="index === columnMap['OMIM']"></tooltip-text>
          <tooltip-text :text="item" :limit=50 v-else-if="index === columnMap['ClinVar']"></tooltip-text>
          <tooltip-text :text="item" :limit=50 v-else-if="index === columnMap['HGMD']"></tooltip-text>
          <tooltip-text :text="item" :limit=20 v-else-if="index === columnMap['gene_info']"></tooltip-text>
          <span v-else> {{ item }}</span>
        </td>
      </template>

      <template slot="actions-append">
        <p class="mt-3 mr-3">Original variants: {{ lastTotalNumberOfVariants }}</p>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import TooltipText from '@/components/TooltipText'
import ColumnDialog from '@/components/ColumnDialog'

export default {
  name: 'GSvarView',
  components: {
    TooltipText,
    ColumnDialog
  },
  data: function () {
    return {
      columnItem: {},
      shouldOpen: false,
      selectedGenes: [],
      rowsPerPage: [
        10,
        20,
        50,
        100,
        { 'text': '$vuetify.dataIterator.rowsPerPageAll', 'value': -1 }
      ]
    }
  },
  computed: {
    columnMap () {
      return this.headers.reduce((result, item, index) => {
        result[item.value] = index
        return result
      }, {})
    }
  },
  methods: {
    openColumnDialog (column) {
      let vm = this
      vm.columnItem = column.reduce((result, item, index) => {
        result[vm.headers[index].text] = item
        return result
      }, {})
      this.shouldOpen = true
    },
    closeDialog () {
      this.shouldOpen = false
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
table { table-layout:fixed; width:50px; word-break:break-all; } /*Setting the table width is important!*/
table td {overflow:hidden;} /*Hide text outside the cell.*/
table td:nth-of-type(1) {width:20px;} /*Setting the width of column 1.*/
table td:nth-of-type(2) {width:30px;} /*Setting the width of column 2.*/
table td:nth-of-type(3) {width:40px;} /*Setting the width of column 3.*/
</style>
