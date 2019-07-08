<template>
  <div>
    <!-- See https://github.com/vuejs-templates/webpack/issues/450#issuecomment-388515010 -->
    <v-btn v-for="item in items" v-bind:key="item.text" @click="openLinksForSelectedGenes(item)" flat>
      <img v-bind:src="require(`@/assets/icons/${item.icon}`)" height="16px" width="16px" class="mr-1">{{ item.text }}
    </v-btn>
  </div>
</template>

<script>
const GENE_ONLY_URLS = ['OMIM', 'GeneCards', 'SysID']

export default {
  name: 'ExternalLinks',
  data () {
    return {
      items: [
        { text: 'OMIM', icon: 'OMIM.png', baseURL: 'https://omim.org/search/?search=' },
        { text: 'GeneCards', icon: 'GeneCards.png', baseURL: 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=' },
        { text: 'UCSC Genome Browser', icon: 'UCSC.png', baseURL: 'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=' },
        { text: 'LOVD', icon: 'LOVD.png', baseURL: 'https://databases.lovd.nl/shared/variants' },
        { text: 'SysID', icon: 'SysID.png', baseURL: 'https://sysid.cmbi.umcn.nl/search?search=' },
        { text: 'VarSome', icon: 'VarSome.png', baseURL: 'https://varsome.com/variant/hg19/' },
        { text: 'Google', icon: 'Google.png', baseURL: 'https://google.com/search?q=' }
      ]
    }
  },
  props: {
    selectedGene: {
      type: Object,
      required: true
    }
  },
  methods: {
    openLinksForSelectedGenes (item) {
      let getURLs = (item, gene) => {
        let tabURLs = []
        if (GENE_ONLY_URLS.includes(item.text)) {
          let genes = gene.gene.split(',')
          genes.forEach((gene) => {
            tabURLs.push(`${item.baseURL}${gene}`)
          })
        } else if (item.text === 'VarSome') {
          tabURLs.push(`${item.baseURL}${gene.chr}-${gene.start}-${gene.ref}-${gene.obs}`)
        } else if (item.text === 'UCSC Genome Browser') {
          tabURLs.push(`${item.baseURL}${gene.chr}:${gene.start}-${gene.end}`)
        } else if (item.text === 'LOVD') {
          tabURLs.push(`${item.baseURL}#search_chromosome=${gene.chr}&search_VariantOnGenome/DNA=${gene.ref.toLowerCase()}.${gene.start}&page_size=100&page=1`)
        } else if (item.text === 'Google') {
          tabURLs.push(`${item.baseURL}${gene.gene}+AND+(${gene.ref}->${gene.obs})`)
        }

        return tabURLs
      }

      getURLs(item, this.selectedGene).forEach((url) => {
        window.open(url, '_blank')
      })
    }
  }
}
</script>
