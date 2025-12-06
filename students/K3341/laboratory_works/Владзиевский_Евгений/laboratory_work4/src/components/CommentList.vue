<template>
  <v-list lines="two" density="comfortable" class="rounded-lg">
    <v-list-item v-for="comment in comments" :key="comment.id">
      <v-list-item-title class="font-weight-semibold">{{ comment.user.name }}</v-list-item-title>
      <v-list-item-subtitle>{{ comment.text }}</v-list-item-subtitle>
      <template #append>
        <v-btn
          v-if="comment.user.id == currentUserId"
          icon="mdi-delete-outline"
          variant="text"
          color="error"
          @click="$emit('delete', comment.id)"
        ></v-btn>
      </template>
    </v-list-item>
  </v-list>
</template>

<script setup>
const props = defineProps({
  comments: {
    type: Array,
    default: () => [],
  },
  currentUserId: {
    type: [String, Number],
    default: null,
  },
})

defineEmits(['delete'])
</script>
