<template>
  <v-card>
    <v-card-text>
      <div class="d-flex align-center">
        <v-avatar
          :color="color"
          size="56"
          class="mr-4"
        >
          <v-icon :icon="icon" size="32" color="white"></v-icon>
        </v-avatar>
        <div class="flex-grow-1">
          <div class="text-caption text-medium-emphasis">{{ title }}</div>
          <div class="text-h5 font-weight-bold">{{ value }}</div>
          <div v-if="subtitle" class="text-caption mt-1">{{ subtitle }}</div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'StatisticsCard',
  props: {
    title: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
    subtitle: {
      type: String,
      default: '',
    },
    icon: {
      type: String,
      default: 'mdi-chart-line',
    },
    color: {
      type: String,
      default: 'primary',
    },
  },
}
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>

