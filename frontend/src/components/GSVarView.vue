<template>
    <v-data-table
        :headers="headers"
        :items="items"
        class="elevation-1"
        :rows-per-page-items="rowsPerPage"
        :loading="loading"
    >
        <template slot="items" slot-scope="props">
            <td v-for="(item, index) in props.item" v-bind:key="index" :bgcolor="getColor(item, index)">{{ item }}</td>
        </template>

        <template slot="actions-append">
            <p class="mt-3 mr-3">Original variants: {{ lastTotalNumberOfVariants }}</p>
        </template>

    </v-data-table>
</template>

<script>
import { produceHeaders } from "@/utils";

/// NOTE: Ported from https://github.com/imgag/ngs-bits/blob/master/src/GSvar/VariantTable.cpp#L114
const colorHeaders = ["gene", "coding_and_splicing", "ClinVar", "HGMD", "NGSD_hom", "NGSD_het", "classification", "validation", "comment"]

export default {
    name: "GSVarView",
    data: function () {
        return {
            rowsPerPage: [
                10,
                25,
                50,
                100
            ]
        }
    },
    computed: {
        headers () {
            return produceHeaders(this.lines.slice(0, 1)[0])
        },
        items () {
            return this.lines.slice(1)
        },
        colorIndexes () {
            let headers = this.headers.map((header) => header.value)
            return headers.filter((header) => colorHeaders.includes(header)).map((header) => headers.indexOf(header))
        }
    },
    methods: {
        getColor(item, index) {
            let color = ''

            if (index === this.colorIndexes[1] && item.includes(':HIGH:')) {
                color = 'red'
            } else if (index === this.colorIndexes[6] && (item === "3" || item === "M")) {
                color = 'orange'
            } else if (index === this.colorIndexes[6] && (item === "4" || item === "5")) {
                color = 'red'
            } else if (index === this.colorIndexes[2] && item.includes("pathogenic")) {
                color = 'red'
            } else if (index === this.colorIndexes[3] && item.includes("CLASS=DM")) {
                color = 'red'
            }

            return color
        }
    },
    props: {
        lastTotalNumberOfVariants: {
            type: Number,
            default: 0
        },
        loading: {
            type: Boolean,
            default: false
        },
        lines: {
            type: Array,
            required: true
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