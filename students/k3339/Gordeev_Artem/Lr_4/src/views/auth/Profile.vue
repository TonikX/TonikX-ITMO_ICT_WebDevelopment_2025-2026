<template>
  <v-container>
    <v-card max-width="600" class="mx-auto mt-4">
      <v-card-title>Настройки профиля</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateProfile">
          <v-text-field
            v-model="form.username"
            label="Имя пользователя"
            readonly
            hint="Для смены имени пользователя обратитесь к администратору"
            persistent-hint
            class="mb-2"
          ></v-text-field>
          
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
          ></v-text-field>

          <v-row>
            <v-col cols="6">
                <v-text-field
                    v-model="form.first_name"
                    label="Имя"
                ></v-text-field>
            </v-col>
            <v-col cols="6">
                <v-text-field
                    v-model="form.last_name"
                    label="Фамилия"
                ></v-text-field>
            </v-col>
          </v-row>


          
          <div class="d-flex justify-end">
             <v-btn color="primary" type="submit" :loading="loading">Сохранить изменения</v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authApi } from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const loading = ref(false)

const form = ref({
    username: '',
    email: '',
    first_name: '',
    last_name: ''
})

onMounted(async () => {
    if (!authStore.user) {
        await authStore.fetchUser()
    }
    if (authStore.user) {
        form.value = { ...authStore.user }
    }
})

const updateProfile = async () => {
    loading.value = true
    try {
        const { username, ...updateData } = form.value
        await authApi.patch('/users/me/', updateData)
        await authStore.fetchUser()
        alertStore.show('Профиль успешно обновлен!', 'success')
    } catch (e) {
        console.error(e)
        alertStore.showError(e)
    } finally {
        loading.value = false
    }
}
</script>
