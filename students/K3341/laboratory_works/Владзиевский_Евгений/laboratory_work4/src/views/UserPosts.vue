<template>
  <div>
    <div class="d-flex align-center mb-4">
      <div>
        <div class="text-h5 font-weight-bold">Посты пользователя</div>
        <div class="text-body-2 text-medium-emphasis" v-if="user">{{ user.name }}</div>
      </div>
      <v-spacer></v-spacer>
      <v-btn variant="text" to="/">Назад</v-btn>
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
      <v-alert v-if="!posts.length" type="info" variant="tonal">У пользователя нет постов</v-alert>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserPosts, likePost, unlikePost, getUserById } from '../api/client'
import PostCard from '../components/PostCard.vue'

const route = useRoute()
const router = useRouter()
const posts = ref([])
const loading = ref(true)
const error = ref('')
const user = ref(null)

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const userId = route.params.id
    const [postsRes, userRes] = await Promise.all([
      getUserPosts({ userId, page: 1, perPage: 20 }),
      getUserById(userId),
    ])
    posts.value = postsRes.items
    user.value = userRes
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить данные пользователя'
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

onMounted(load)
watch(() => route.params.id, load)
</script>
