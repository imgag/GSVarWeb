<template>
    <v-toolbar flat>
        <v-spacer></v-spacer>
        <!-- See https://github.com/vuejs-templates/webpack/issues/450#issuecomment-388515010 -->
        <v-btn v-for="item in items" v-bind:key="item.text" @click="openLinksForSelectedGenes(item)">
            <img v-bind:src="require(`@/assets/icons/${item.icon}`)" height="16px" width="16px" class="mr-1">{{ item.text }}
        </v-btn>
    </v-toolbar>
</template>

<script>
const GENE_ONLY_URLS = ['OMIM', 'GeneCards', 'SysID']

export default {
    name: "ExternalLinks",
    data () {
      return {
          items: [
              { text: 'OMIM', icon: 'OMIM.png', baseURL: 'https://omim.org/search/?search=' },
              { text: 'GeneCards', icon: 'GeneCards.png', baseURL: 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=' },
              { text: 'UCSC Genome Browser', icon: 'UCSC.png', baseURL: 'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=' },
              { text: 'LOVD', icon: 'LOVD.png', baseURL: 'https://databases.lovd.nl/shared/variants' },
              { text: 'SysID', icon: 'SysID.png', baseURL: 'https://sysid.cmbi.umcn.nl/search?search=' },
              { text: 'VarSome', icon: 'VarSome.png', baseURL: 'https://varsome.com/variant/hg19/' }
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
        openLinksForSelectedGenes(item) {
            let selectedGenesSet = new Set(this.selectedGenes)
            let getURL = (item, gene) => {
                let tabURL = ''
                if (GENE_ONLY_URLS.includes(item.text)) {
                    tabURL = `${item.baseURL}${gene.gene}`
                } else if (item.text === 'VarSome') {
                    tabURL = `${item.baseURL}${gene.chr}-${gene.start}-${gene.ref}-${gene.obs}`
                } else if (item.text === 'UCSC Genome Browser') {
                    tabURL = `${item.baseURL}${gene.chr}:${gene.start}-${gene.end}`
                } else if (item.text === 'LOVD') {
                    tabURL = `${item.baseURL}#search_chromosome=${gene.chr}&search_VariantOnGenome/DNA=${gene.ref.toLowerCase()}.${gene.start}&page_size=100&page=1`
                }

                return tabURL
            }

            selectedGenesSet.forEach((gene) => {
                window.open(getURL(item, gene), '_blank')
            })
        }
    }
}
</script>
