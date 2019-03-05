<template>
    <v-stepper v-model="step">
        <v-stepper-header>
            <v-stepper-step :complete="step > 1" step="1">Select GSVar file</v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="step > 2" step="2">Select filters</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
            <v-stepper-content step="1">
                <v-input
                        type="file"
                        hint="Select file"
                        persistent-hint
                        class="mb-3"
                >
                <input
                        type="file"
                        @change="selectedFile = $event.srcElement"
                        accept=".GSvar"
                />
                </v-input>

                <v-btn
                        color="primary"
                        @click="updateSelectedFile"
                        :disabled="selectedFile === null"
                >
                    Continue
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="2">
                <v-select
                        v-model="selectedFilterName"
                        :items="filterNames"
                        hint="Select filter"
                        persistent-hint
                        class="mb-3"
                ></v-select>

                <v-btn
                        color="primary"
                        @click="applyFilter"
                >
                    Apply filter
                </v-btn>

                <v-btn flat @click="step = 1">Select file</v-btn>
            </v-stepper-content>
        </v-stepper-items>
    </v-stepper>
</template>

<script>
export default {
    name: "FilterSelect",
    data: function () {
        return {
            step: 1,
            selectedFile: null,
            selectedFilterName: ""
        }
    },
    methods: {
        updateSelectedFile () {
            this.step = 2
            if (this.selectedFile) this.$emit('updateSelectedFile', this.selectedFile)
        },
        applyFilter () {
            this.$emit('applyFilter', this.selectedFilterName)
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
