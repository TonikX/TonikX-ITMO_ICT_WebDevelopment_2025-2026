<template>
  <div>
    <div class="d-flex align-center mb-4">
      <div class="text-h5 font-weight-bold">Мои посты</div>
      <v-spacer></v-spacer>
      <v-btn variant="tonal" color="primary" to="/create" prepend-icon="mdi-pencil">Написать</v-btn>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

    <v-skeleton-loader v-if="loading" type="card, card"></v-skeleton-loader>

    <div v-else>
      <PostCard
        v-for="item in posts"
        :key="item.id"
        :post="item"
        @open="openPost"
        @like="toggleLike"
      />
      <v-alert v-if="!posts.length" type="info" variant="tonal">Постов пока нет</v-alert>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { getUserPosts, likePost, unlikePost } from '../api/client'
import { currentUserId } from '../stores/auth'
import PostCard from '../components/PostCard.vue'

const router = useRouter()
const posts = ref([])
const loading = ref(true)
const error = ref('')
const ownerId = ref(null)

const load = async () => {
  if (!ownerId.value) return
  loading.value = true
  error.value = ''
  try {
    const data = await getUserPosts({ userId: ownerId.value, page: 1, perPage: 20 })
    posts.value = data.items
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить посты'
  } finally {
    loading.value = false
  }
}

const toggleLike = async (post) => {
  try {
    if (post.is_liked) {
      await unlikePost(post.id)
      post.is_liked = false
      post.like_count = Math.max(0, (post.like_count || 0) - 1)
    } else {
      await likePost(post.id)
      post.is_liked = true
      post.like_count = (post.like_count || 0) + 1
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось изменить лайк'
  }
}

const openPost = (id) => router.push({ name: 'post', params: { id } })

watchEffect(() => {
  const id = currentUserId()
  if (id) {
    ownerId.value = id
    load()
  }
})
</script>
