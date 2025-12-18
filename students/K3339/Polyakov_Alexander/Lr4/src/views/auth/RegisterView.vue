<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

const auth = useAuthStore()
const router = useRouter()
const formRef = ref()
const form = reactive({
  username: '',
  email: '',
  password: '',
})
const errorMessage = ref('')

const handleRegister = async () => {
  const valid = await formRef.value?.validate()
  if (!valid) return
  try {
    await auth.register(form)
    router.push('/')
  } catch {
    errorMessage.value = auth.error || 'Registration failed'
  }
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card elevation="6" width="460">
      <v-card-title class="text-h5">Create account</v-card-title>
      <v-card-text>
        <v-form ref="formRef" @submit.prevent="handleRegister">
          <v-text-field
            v-model="form.username"
            label="Username"
            prepend-inner-icon="mdi-account"
            :rules="[(v) => !!v || 'Required']"
            required
          />
          <v-text-field
            v-model="form.email"
            label="Email"
            prepend-inner-icon="mdi-email"
            type="email"
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
            Register and sign in
          </v-btn>
          <div class="text-center">
            <RouterLink to="/login">Have an account? Sign in</RouterLink>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

