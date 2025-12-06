<template>
  <div>
    <v-btn variant="text" prepend-icon="mdi-arrow-left" class="mb-4" @click="router.back()">Назад</v-btn>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

    <v-skeleton-loader v-if="loading" type="card"></v-skeleton-loader>

    <div v-else-if="post">
      <v-card variant="flat" class="pa-4 mb-4" color="white">
        <div class="d-flex align-center mb-2">
          <div>
            <div class="text-h5 font-weight-bold">{{ post.title }}</div>
            <div class="text-body-2 text-medium-emphasis">
              Автор:
              <RouterLink :to="{ name: 'userPosts', params: { id: post.user.id } }">{{ post.user.name }}</RouterLink>
            </div>
          </div>
          <v-spacer></v-spacer>
          <v-btn
            :color="post.is_liked ? 'primary' : undefined"
            variant="tonal"
            @click="toggleLike(post)"
            prepend-icon="mdi-thumb-up"
          >
            {{ post.like_count }}
          </v-btn>
        </div>
        <div class="text-body-1 mb-4">{{ post.text }}</div>

        <v-row v-if="post.images?.length" dense>
          <v-col v-for="img in post.images" :key="img.url || img.hash" cols="12" sm="6" md="4">
            <SecureImage :image="img" aspect-ratio="1.6" img-class="rounded-lg border" />
          </v-col>
        </v-row>
      </v-card>

      <v-card class="pa-4" variant="outlined">
        <div class="d-flex align-center mb-3">
          <div class="text-subtitle-1 font-weight-bold">Комментарии ({{ comments.length }})</div>
          <v-spacer></v-spacer>
        </div>

        <CommentList :comments="comments" :current-user-id="userId" @delete="deleteComment"></CommentList>

        <v-divider class="my-4"></v-divider>
        <v-form @submit.prevent="submitComment">
          <v-textarea
            v-model="commentText"
            label="Оставить комментарий"
            rows="2"
            auto-grow
            required
          ></v-textarea>
          <v-btn :loading="commentLoading" color="primary" type="submit" prepend-icon="mdi-send" class="mt-2">
            Отправить
          </v-btn>
        </v-form>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import CommentList from '../components/CommentList.vue'
import { addComment, fetchComments, getPostById, likePost, removeComment, unlikePost } from '../api/client'
import SecureImage from '../components/SecureImage.vue'
import { currentUserId } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const comments = ref([])
const loading = ref(true)
const error = ref('')
const commentText = ref('')
const commentLoading = ref(false)
const userId = currentUserId()

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const id = route.params.id
    const [postRes, commentsRes] = await Promise.all([
      getPostById(id),
      fetchComments(id, { page: 1, perPage: 50 }),
    ])
    post.value = postRes
    comments.value = commentsRes.items
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось загрузить пост'
  } finally {
    loading.value = false
  }
}

const toggleLike = async (item) => {
  try {
    if (item.is_liked) {
      await unlikePost(item.id)
      item.is_liked = false
      item.like_count = Math.max(0, (item.like_count || 0) - 1)
    } else {
      await likePost(item.id)
      item.is_liked = true
      item.like_count = (item.like_count || 0) + 1
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось изменить лайк'
  }
}

const submitComment = async () => {
  if (!commentText.value.trim()) return
  commentLoading.value = true
  try {
    const newComment = await addComment(post.value.id, commentText.value)
    comments.value = [...comments.value, newComment]
    commentText.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось добавить комментарий'
  } finally {
    commentLoading.value = false
  }
}

const deleteComment = async (commentId) => {
  try {
    await removeComment(post.value.id, commentId)
    comments.value = comments.value.filter((c) => c.id !== commentId)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Не удалось удалить комментарий'
  }
}

onMounted(load)
</script>
