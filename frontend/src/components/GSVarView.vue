<template>
    <v-data-table
        :headers="headers"
        :items="items"
        class="elevation-1"
        :rows-per-page-items="rowsPerPage"
        :loading="loading"
        select-all
    >
        <template slot="items" slot-scope="props">
            <td>
                <v-checkbox
                    primary
                    @change="updateGene(props.item, $event)"
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
import TooltipText from "@/components/TooltipText"

/// Ported from https://github.com/imgag/ngs-bits/blob/master/src/GSvar/VariantTable.cpp#L114
/// Since the headers are sorted this array also needs to be sorted by index!
const colorHeaders = ["gene", "coding_and_splicing", "ClinVar", "HGMD", "NGSD_hom", "NGSD_het", "classification", "validation", "comment"]

export default {
    name: "GSVarView",
    components: {
        TooltipText,
    },
    data: function () {
        return {
            selectedGenes: [],
            rowsPerPage: [
                10,
                25,
                50,
                100
            ]
        }
    },
    computed: {
        colorIndexes () {
            let headers = this.$store.getters.headers.map((header) => header.value)
            return headers.filter((header) => colorHeaders.includes(header)).map((header) => headers.indexOf(header))
        },
        colorMap () {
            return this.colorIndexes.reduce((result, item, index) => {
                result[colorHeaders[index]] = item
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
        updateGene (column, selected) {
            let gene = column[this.colorMap["gene"]]
            if (selected) {
                this.selectedGenes.push(gene)
            } else {
                let geneIndex = this.selectedGenes.indexOf(gene)
                if (geneIndex > -1) this.selectedGenes.splice(geneIndex, 1)
            }
        },
        getColor(item, index) {
            let color = ''

            // warning
            if (index === this.colorMap["coding_and_splicing"] && item.includes(':HIGH:')) {
                color = 'red'
            }

            if (index === this.colorMap["classification"] && (item === "3" || item === "M")) {
                color = 'orange'
            } else if (index === this.colorMap["classification"] && (item === "4" || item === "5")) {
                color = 'red'
            } else if (index === this.colorMap["classification"] && item.includes("pathogenic")) {
                color = 'red'
            } else if (index === this.colorMap["classification"] && item.includes("CLASS=DM")) {
                color = 'red'
            }

            if (index === this.colorMap["classification"] && (item === "0" || item === "1" || item === "2")) {   // non-pathogenic
                color = 'green'
            }

            // highlighted
            if (index === this.colorMap["validation"] && item.includes("TP")) {
                color = 'yellow'
            } else if (index === this.colorMap["comment"] && item !== "") {
                color = 'yellow'
            } else if (index === this.colorMap["NGSD_hom"] && item === "0") {
                color = 'yellow'
            } else if (index === this.colorMap["NGSD_het"] && item === "1") {
                color = 'yellow'
            } else if (index === this.colorMap["ClinVar"] && item.includes("confirmed")) {
                color = 'yellow'
            } //else if (index === this.colorMap["genes"]) /// TODO: Deal with imprinting genes

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