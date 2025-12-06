<template>
  <v-card class="mb-4" variant="outlined">
    <v-card-title class="d-flex align-center justify-space-between">
      <div>
        <div class="text-subtitle-1 font-weight-bold">{{ post.title }}</div>
        <div class="text-body-2 text-medium-emphasis">
          от
          <RouterLink :to="{ name: 'userPosts', params: { id: post.user.id } }" class="font-weight-medium">
            {{ post.user.name }}
          </RouterLink>
        </div>
      </div>
      <v-btn variant="text" icon="mdi-open-in-new" @click="$emit('open', post.id)"></v-btn>
    </v-card-title>
    <v-card-text>
      <div class="text-body-1 mb-4">{{ post.text }}</div>
      <v-row v-if="post.images?.length" dense>
        <v-col v-for="img in post.images" :key="img.url || img.hash || img" cols="12" sm="6" md="4">
          <SecureImage :image="img" aspect-ratio="1.6" img-class="rounded-lg" />
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions class="d-flex justify-space-between">
      <div>
        <v-btn :color="post.is_liked ? 'primary' : undefined" variant="tonal" @click="$emit('like', post)">
          <v-icon start>{{ post.is_liked ? 'mdi-thumb-up' : 'mdi-thumb-up-outline' }}</v-icon>
          {{ post.like_count || 0 }}
        </v-btn>
        <v-btn variant="text" @click="$emit('open', post.id)">
          <v-icon start>mdi-comment-outline</v-icon>
          {{ post.comment_count || 0 }} коммент.
        </v-btn>
      </div>
      <slot></slot>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import SecureImage from './SecureImage.vue'

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

defineEmits(['open', 'like'])
</script>
