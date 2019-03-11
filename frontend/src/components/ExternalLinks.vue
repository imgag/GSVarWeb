<template>
    <v-toolbar flat>
        <v-spacer></v-spacer>
        <!-- See https://github.com/vuejs-templates/webpack/issues/450#issuecomment-388515010 -->
        <v-btn v-for="item in items" v-bind:key="item.text" @click="openLinksForSelectedGenes(item.baseURL)">
            <img v-bind:src="require(`@/assets/icons/${item.icon}`)" height="16px" width="16px" class="mr-1">{{ item.text }}
        </v-btn>
    </v-toolbar>
</template>

<script>
export default {
    name: "ExternalLinks",
    data () {
      return {
          items: [
              { text: 'OMIM', icon: 'OMIM.png', baseURL: 'https://omim.org/search/?search=' },
              { text: 'GeneCards', icon: 'GeneCards.png', baseURL: 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=' },
              { text: 'UCSC Genome Browser', icon: 'UCSC.png' },
              { text: 'LOVD', icon: 'LOVD.png' },
              { text: 'SysID', icon: 'SysID.png' },
              { text: 'VarSome', icon: 'VarSome.png' }
          ]
      }
    },
    props: {
        selectedGenes: {
            type: Array,
            required: true
        }
    },
    methods: {
        openLinksForSelectedGenes(baseUrl) {
            let selectedGenesSet = new Set(this.selectedGenes)

            selectedGenesSet.forEach((gene) => {
                window.open(`${baseUrl}${gene}`, '_blank')
            })
        }
    }
}
</script>
