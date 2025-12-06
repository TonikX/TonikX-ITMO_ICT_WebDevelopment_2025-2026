<template>
  <div>
    <div class="d-flex align-center mb-4">
      <div class="text-h5 font-weight-bold">Лента</div>
      <v-spacer></v-spacer>
      <v-btn variant="tonal" color="primary" to="/create" prepend-icon="mdi-pencil">Новый пост</v-btn>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

    <v-skeleton-loader v-if="loading" type="card, card, card" class="mb-4"></v-skeleton-loader>

    <div v-else>
      <PostCard
        v-for="item in posts"
        :key="item.id"
        :post="item"
        @open="openPost"
        @like="toggleLike"
      />
      <v-pagination
        v-if="totalPages > 1"
        v-model="page"
        :length="totalPages"
        class="mt-4"
        @update:model-value="load"
      ></v-pagination>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getLatestPosts, likePost, unlikePost } from '../api/client'
import PostCard from '../components/PostCard.vue'

const router = useRouter()
const posts = ref([])
const loading = ref(true)
const error = ref('')
const page = ref(1)
const perPage = 5
const total = ref(0)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / perPage)))

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const data = await getLatestPosts({ page: page.value, perPage })
    posts.value = data.items
    total.value = data.count
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить посты'
  } finally {
    loading.value = false
  }
}

const openPost = (id) => router.push({ name: 'post', params: { id } })

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

onMounted(load)
</script>
