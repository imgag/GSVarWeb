<template>
  <div>
    <column-dialog v-if="shouldOpen" @close="closeDialog" :item="columnItem"></column-dialog>
    <ag-grid-vue
        style="width: 100%; height: 80vmin;"
        class="ag-theme-material"
        @rowClicked="openColumnDialog"
        :columnDefs="mergedColorHeaders(headers)"
        :rowData="items.map((column) => reduceColumnToObject(column))"
        :pagination="true"
    />
  </div>
</template>

<script>
import ColumnDialog from '@/components/ColumnDialog'
import { AgGridVue } from 'ag-grid-vue'
import 'ag-grid-community/dist/styles/ag-grid.css'
import 'ag-grid-community/dist/styles/ag-theme-material.css'

export default {
  name: 'GSvarView',
  components: {
    AgGridVue,
    ColumnDialog
  },
  data: function () {
    return {
      columnItem: {},
      shouldOpen: false
    }
  },
  computed: {
    columnMap () {
      return this.headers.reduce((result, item, index) => {
        result[item.field] = index
        return result
      }, {})
    }
  },
  methods: {
    openColumnDialog (row) {
      this.columnItem = row.data // TODO: Rename ColumnDialog -> RowDialog
      this.shouldOpen = true
    },
    closeDialog () {
      this.shouldOpen = false
    },
    reduceColumnToObject (column) {
      let vm = this
      return column.reduce((result, item, index) => {
        result[vm.headers[index].headerName] = item
        return result
      }, {})
    },
    /// Ported from https://github.com/imgag/ngs-bits/blob/master/src/GSvar/VariantTable.cpp#L114
    mergedColorHeaders (headers) {
      headers[this.columnMap['coding_and_splicing']]['cellClassRules'] = {
        'rag-red': (params) => params.value.includes(':HIGH:')
      }
      // TODO: Handle virtual color calculations
      // headers[this.columnMap['classification']]['cellClassRules'] = {
      //   'rag-orange': (params) => (params.value === '3' || params.value === 'M'),
      //   'rag-red': (params) => (params.value === '4' || params.value === '5' || params.value.includes('pathogenic') || params.value.includes('CLASS=DM')),
      //   'rag-green': (params) => (params.value === '0' || params.value === '1' || params.value === '2') // non-pathogenic
      // }
      // headers[this.columnMap['validation']]['cellClassRules'] = {
      //   'rag-yellow': (params) => params.value.includes('TP')
      // }
      // headers[this.columnMap['comment']]['cellClassRules'] = {
      //   'rag-yellow': (params) => params.value !== ''
      // }
      // headers[this.columnMap['NGSD_hom']]['cellClassRules'] = {
      //   'rag-yellow': (params) => params.value !== '0'
      // }
      // headers[this.columnMap['NGSD_het']]['cellClassRules'] = {
      //   'rag-yellow': (params) => params.value !== '1'
      // }
      headers[this.columnMap['ClinVar']]['cellClassRules'] = {
        'rag-yellow': (params) => params.value.includes('confirmed')
      }

      return headers
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
