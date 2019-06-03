<template>
    <span v-if="text.length < 100">
        {{ text }}
    </span>
    <v-tooltip
            bottom
            v-else
            nudge-width="300px"
    >
        <template v-slot:activator="{ on }">
            <span v-on="on">{{ text.substr(0, limit) }}</span>
        </template>
        <span>
          <ul>
            <li v-for="(item, index) in text.split(this.separator)" v-bind:key="index">{{ item }}</li>
          </ul>
        </span>
    </v-tooltip>
</template>

<script>
export default {
  name: 'TooltipText',
  props: {
    limit: {
      type: Number,
      default: 100
    },
    separator: {
      type: String,
      default: ','
    },
    text: {
      type: String,
      required: true
    }
  }
}
</script>
