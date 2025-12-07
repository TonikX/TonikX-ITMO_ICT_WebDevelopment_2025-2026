<template>
  <v-chip
    :color="priorityColor"
    :size="size"
    variant="flat"
  >
    {{ priorityLabel }}
  </v-chip>
</template>

<script>
import { getRequestPriorityLabel, getRequestPriorityColor } from '@/utils/statusUtils'

export default {
  name: 'PriorityChip',
  props: {
    priority: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      default: 'default',
    },
  },
  computed: {
    priorityLabel() {
      return getRequestPriorityLabel(this.priority)
    },
    priorityColor() {
      return getRequestPriorityColor(this.priority)
    },
  },
}
</script>

