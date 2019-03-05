<template>
    <v-data-table
        :headers="headers"
        :items="items"
        class="elevation-1"
        :rows-per-page-items="rowsPerPage"
        :loading="loading"
    >
        <template slot="items" slot-scope="props">
            <td v-for="(item, index) in props.item" v-bind:key="index">{{ item }}</td>
        </template>

    </v-data-table>
</template>

<script>
import { produceHeaders } from "@/utils";

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
        }
    },
    props: {
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