<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4">Добро пожаловать!</v-card-title>
          <v-card-text>
            <p class="text-h6">Вы успешно вошли в систему управления отелем</p>
            <v-divider class="my-4"></v-divider>
            <v-row>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Типы номеров</v-card-title>
                  <v-card-text>
                    <p>Управление типами номеров и просмотр статистики</p>
                    <v-btn color="primary" to="/room-types">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Этажи</v-card-title>
                  <v-card-text>
                    <p>Управление этажами и просмотр статистики</p>
                    <v-btn color="primary" to="/floors">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Номера</v-card-title>
                  <v-card-text>
                    <p>Управление номерами отеля</p>
                    <v-btn color="primary" to="/rooms">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Гости</v-card-title>
                  <v-card-text>
                    <p>Управление информацией о гостях</p>
                    <v-btn color="primary" to="/guests">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Проживания</v-card-title>
                  <v-card-text>
                    <p>Управление проживаниями и просмотр сводки</p>
                    <v-btn color="primary" to="/stays">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>Сотрудники</v-card-title>
                  <v-card-text>
                    <p>Управление сотрудниками отеля</p>
                    <v-btn color="primary" to="/employees">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card class="mb-3" variant="outlined">
                  <v-card-title>График уборки</v-card-title>
                  <v-card-text>
                    <p>Управление графиком уборки помещений</p>
                    <v-btn color="primary" to="/cleaning">Перейти</v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-divider class="my-4"></v-divider>
            <v-btn color="primary" to="/profile" class="mr-2">
              Профиль
            </v-btn>
            <v-btn color="error" @click="handleLogout">
              Выйти
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'

const router = useRouter()

const handleLogout = async () => {
  try {
    await authAPI.logout()
    localStorage.removeItem('auth_token')
    router.push('/login')
  } catch (err) {
    console.error('Ошибка при выходе:', err)
    localStorage.removeItem('auth_token')
    router.push('/login')
  }
}
</script>


