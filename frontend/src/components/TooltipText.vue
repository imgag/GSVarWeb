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
            <span v-on="on">{{ text.substr(0, 100).replace(" ", "&nbsp;") }}</span>
        </template>
        <span>{{ text }}</span>
    </v-tooltip>
</template>

<script>
export default {
  name: 'TooltipText',
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>
