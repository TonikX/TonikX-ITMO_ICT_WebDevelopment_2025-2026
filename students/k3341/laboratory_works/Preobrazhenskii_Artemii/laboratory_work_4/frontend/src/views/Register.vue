<template>
  <v-container>
    <v-card class="mx-auto" max-width="520">
      <v-card-title>Register</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit">
          <v-alert v-if="error" type="error" dense class="mb-3">{{ error }}</v-alert>
          <v-text-field label="Username" v-model="username" required />
          <v-text-field label="Email" v-model="email" required />
          <v-text-field label="Password" v-model="password" type="password" required />
          <v-btn type="submit" block color="primary">Register</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

export default {
  setup () {
    const username = ref('')
    const email = ref('')
    const password = ref('')
    const error = ref(null)
    const router = useRouter()

    const submit = async () => {
      error.value = null
      try {
        await api.post('/auth/users/', { username: username.value, email: email.value, password: password.value })
        const loginRes = await api.post('/auth/jwt/create/', { username: username.value, password: password.value })
        if (loginRes.data.access) {
          localStorage.setItem('token', loginRes.data.access)
          api.setAuth(loginRes.data.access)
          router.push({ name: 'file-list' })
        }
      } catch (e) {
        const resp = e.response && e.response.data
        if (resp) {
          if (resp.detail) error.value = resp.detail
          else if (typeof resp === 'string') error.value = resp
          else error.value = Object.entries(resp).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ')
        } else {
          error.value = 'Register failed'
        }
      }
    }
    return { username, email, password, submit, error }
  }
}
</script>