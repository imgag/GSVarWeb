<template>
    <v-form>
        <v-container>
            <v-layout>
                <v-flex
                        xs12
                        md4
                >
                    <v-input
                            type="file"
                            hint="Select file"
                            persistent-hint
                    >
                        <input type="file"/>
                    </v-input>
                </v-flex>

                <v-flex
                    xs12
                    md4
                >
                    <v-select
                        v-model="selectedFilterNames"
                        :items="filterNames"
                        multiple
                        hint="Select filters"
                        persistent-hint
                    ></v-select>
                </v-flex>

                <v-flex
                        xs12
                        md4
                >
                    <v-btn disabled>Apply filter</v-btn>
                </v-flex>
            </v-layout>
        </v-container>
    </v-form>
</template>

<script>
export default {
    name: "FilterSelect",
    data: function () {
        return {
            selectedFile: null,
            selectedFilterNames: []
        }
    },
    props: {
        filterNames: {
            type: Array,
            required: true
        }
    }
}
</script>

<style scoped>

</style>