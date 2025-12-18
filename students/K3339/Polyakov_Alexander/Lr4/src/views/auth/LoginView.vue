<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const formRef = ref()
const form = reactive({
  username: '',
  password: '',
})
const errorMessage = ref('')

const handleLogin = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  try {
    await auth.login(form)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch {
    errorMessage.value = auth.error || 'Login failed'
  }
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card elevation="6" width="420">
      <v-card-title class="text-h5">Sign In</v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="handleLogin">
          <v-text-field
            v-model="form.username"
            label="Username"
            prepend-inner-icon="mdi-account"
            :rules="[(v) => !!v || 'Required']"
            required
          />
          <v-text-field
            v-model="form.password"
            label="Password"
            type="password"
            prepend-inner-icon="mdi-lock"
            :rules="[(v) => !!v || 'Required']"
            required
          />

          <v-alert
            v-if="errorMessage"
            type="error"
            variant="tonal"
            density="comfortable"
            class="mb-4"
          >
            {{ errorMessage }}
          </v-alert>

          <v-btn
            color="primary"
            block
            :loading="auth.loading"
            type="submit"
            class="mb-2"
          >
            Sign in
          </v-btn>
          <div class="text-center">
            <RouterLink to="/register">No account? Register</RouterLink>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

