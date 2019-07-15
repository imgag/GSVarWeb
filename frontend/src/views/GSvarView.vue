<template>
  <div>
    <column-dialog v-if="shouldOpen" @close="closeDialog" :item="columnItem"></column-dialog>
    <ag-grid-vue
        style="width: 100%; height: 80vmin;"
        class="ag-theme-material"
        @rowClicked="openColumnDialog"
        :columnDefs="columnDefs(headers)"
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
    columnDefs (headers) {
      headers[this.columnMap['coding_and_splicing']]['cellClassRules'] = {
        'red': (params) => params.value.includes(':HIGH:')
      }
      headers[this.columnMap['HGMD']]['cellClassRules'] = {
        'red': (params) => params.value.includes('CLASS=DM')
      }
      headers[this.columnMap['ClinVar']]['cellClassRules'] = {
        'red': (params) => params.value.includes('pathogenic') && !params.value.includes('conflicting interpretations of pathogenicity'),
        'yellow': (params) => params.value.includes('(confirmed)')
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
