<template>
  <v-chip
    :color="statusColor"
    :size="size"
    variant="flat"
  >
    {{ statusLabel }}
  </v-chip>
</template>

<script>
import { getRequestStatusLabel, getRequestStatusColor } from '@/utils/statusUtils'

export default {
  name: 'StatusChip',
  props: {
    status: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      default: 'default',
    },
  },
  computed: {
    statusLabel() {
      return getRequestStatusLabel(this.status)
    },
    statusColor() {
      return getRequestStatusColor(this.status)
    },
  },
}
</script>

