<template>
  <v-container>
    <v-card class="mx-auto" max-width="480">
      <v-card-title>Login</v-card-title>
      <v-card-text>
            <v-form @submit.prevent="submit">
              <v-alert v-if="error" type="error" dense class="mb-3">{{ error }}</v-alert>
              <v-text-field label="Username" v-model="username" required />
              <v-text-field label="Password" v-model="password" type="password" required />
              <v-btn type="submit" block color="primary">Login</v-btn>
            </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

export default {
  setup () {
    const username = ref('')
    const password = ref('')
    const error = ref(null)
    const auth = useAuthStore()
    const router = useRouter()

    const submit = async () => {
      error.value = null
      try {
        await auth.login(username.value, password.value)
        await auth.fetchMe()
        router.push({ name: 'files' })
      } catch (e) {
        // Try to extract detailed error messages from API response
        const resp = e.response && e.response.data
        if (resp) {
          if (resp.detail) error.value = resp.detail
          else if (typeof resp === 'string') error.value = resp
          else error.value = Object.entries(resp).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ')
        } else {
          error.value = 'Login failed'
        }
      }
    }

    return { username, password, submit, error }
  }
}
</script>