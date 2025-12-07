<template>
  <v-container>
    <v-card class="mx-auto" max-width="640">
      <v-card-title>Account Settings</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="saveProfile">
          <v-alert v-if="profileError" type="error" dense class="mb-3">{{ profileError }}</v-alert>
          <v-alert v-if="profileSuccess" type="success" dense class="mb-3">{{ profileSuccess }}</v-alert>
          <v-text-field label="Username" v-model="form.username" required />
          <v-text-field label="Email" v-model="form.email" required />
          <v-btn type="submit" color="primary">Save</v-btn>
        </v-form>

        <v-divider class="my-4" />

        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>Change Password</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-form @submit.prevent="savePassword">
                 <v-alert v-if="passwordError" type="error" dense class="mb-3">{{ passwordError }}</v-alert>
                 <v-alert v-if="passwordSuccess" type="success" dense class="mb-3">{{ passwordSuccess }}</v-alert>
                 <v-text-field label="Current Password" v-model="currentPassword" type="password" required />
                 <v-text-field label="New Password" v-model="newPassword" type="password" required />
                 <v-text-field label="Confirm New Password" v-model="confirmPassword" type="password" required />
                 <v-btn type="submit" color="error">Change Password</v-btn>
              </v-form>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

export default {
  setup () {
    const auth = useAuthStore()
    const router = useRouter()

    const form = reactive({ username: '', email: '' })
    const currentPassword = ref('')
    const newPassword = ref('')
    const confirmPassword = ref('')

    onMounted(() => {
      if (!auth.isAuthenticated) return router.push({ name: 'login' })
      if (auth.user) {
        form.username = auth.user.username || ''
        form.email = auth.user.email || ''
      } else {
        auth.fetchMe().then(() => {
          form.username = auth.user?.username || ''
          form.email = auth.user?.email || ''
        }).catch(() => {})
      }
    })

    const profileError = ref(null)
    const profileSuccess = ref(null)

    const saveProfile = async () => {
      profileError.value = null
      profileSuccess.value = null
      try {
        await auth.updateProfile({ username: form.username, email: form.email })
        profileSuccess.value = 'Profile updated'
      } catch (e) {
        console.error(e)
        const resp = e.response && e.response.data
        if (resp) {
          if (resp.detail) profileError.value = resp.detail
          else profileError.value = Object.entries(resp).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ')
        } else profileError.value = 'Failed to update profile'
      }
    }

    const passwordError = ref(null)
    const passwordSuccess = ref(null)

    const savePassword = async () => {
      passwordError.value = null
      passwordSuccess.value = null
      if (newPassword.value !== confirmPassword.value) return passwordError.value = 'Passwords do not match'
      try {
        await auth.changePassword(currentPassword.value, newPassword.value)
        currentPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
        passwordSuccess.value = 'Password changed'
      } catch (e) {
        console.error(e)
        const resp = e.response && e.response.data
        if (resp) {
          if (resp.detail) passwordError.value = resp.detail
          else passwordError.value = Object.entries(resp).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join(' | ')
        } else passwordError.value = 'Failed to change password'
      }
    }

    return { form, currentPassword, newPassword, confirmPassword, saveProfile, savePassword, profileError, profileSuccess, passwordError, passwordSuccess }
  }
}
</script>

