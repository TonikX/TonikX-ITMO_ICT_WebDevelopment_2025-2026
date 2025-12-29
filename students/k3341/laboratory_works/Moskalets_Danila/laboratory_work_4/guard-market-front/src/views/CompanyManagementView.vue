<template>
  <div>
    <!-- Уведомление об успехе -->
    <SuccessNotification
        :show="successSnackbar.show"
        :text="successSnackbar.text"
        :color="successSnackbar.color"
        :icon="successSnackbar.icon"
        @close="successSnackbar.show = false"
    />

    <!-- Загрузка -->
    <div v-if="isLoading" class="text-center py-10">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
      <p class="mt-4">Загрузка данных компании...</p>
    </div>

    <!-- Нет компании -->
    <div v-else-if="!authStore.hasCompany">
      <v-card class="pa-6 text-center">
        <v-icon size="100" color="warning" class="mb-4">mdi-office-building-off</v-icon>
        <h2 class="text-h4 mb-4">У вас нет компании</h2>
        <p class="text-body-1 mb-6">
          Чтобы управлять компанией, сначала создайте её в своем профиле
        </p>
        <v-btn to="/profile" color="primary" size="large">
          <v-icon start icon="mdi-account"></v-icon>
          Перейти в профиль
        </v-btn>
      </v-card>
    </div>

    <!-- Основной контент управления компанией -->
    <div v-else>
      <!-- Заголовок -->
      <v-row class="mb-6">
        <v-col cols="12">
          <v-card class="pa-6">
            <div class="d-flex align-center justify-space-between">
              <div>
                <v-card-title class="text-h4 mb-2">
                  Управление компанией
                </v-card-title>
                <v-card-subtitle class="text-body-1">
                  {{ company.name }} – панель администратора
                </v-card-subtitle>
              </div>
              <div class="d-flex align-center">
                <v-chip
                    v-if="company.average_rating"
                    color="amber"
                    text-color="white"
                    size="large"
                    class="mr-3"
                >
                  <v-icon start icon="mdi-star"></v-icon>
                  {{ company.average_rating.toFixed(1) }}
                </v-chip>
                <v-btn
                    :to="`/companies/${company.id}`"
                    color="primary"
                    variant="outlined"
                >
                  <v-icon start icon="mdi-eye"></v-icon>
                  Публичная страница
                </v-btn>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Вкладки управления -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-tabs v-model="activeTab" color="primary" grow>
              <v-tab value="info">
                <v-icon start icon="mdi-information"></v-icon>
                Информация
              </v-tab>
              <v-tab value="services">
                <v-icon start icon="mdi-tools"></v-icon>
                Услуги
                <v-badge
                    v-if="company.services?.length"
                    :content="company.services.length"
                    color="primary"
                    inline
                    class="ml-2"
                ></v-badge>
              </v-tab>
              <v-tab value="requests">
                <v-icon start icon="mdi-format-list-bulleted"></v-icon>
                Заявки
                <v-badge
                    v-if="company.service_requests?.length"
                    :content="company.service_requests.length"
                    color="primary"
                    inline
                    class="ml-2"
                ></v-badge>
              </v-tab>
              <v-tab value="discounts">
                <v-icon start icon="mdi-sale"></v-icon>
                Скидки
              </v-tab>
            </v-tabs>

            <v-card-text class="pa-0">
              <!-- Информация о компании -->
              <v-window v-model="activeTab">
                <v-window-item value="info">
                  <CompanyInfoTab
                      :company="company"
                      @company-updated="loadCompanyData"
                      @open-delete-dialog="deleteCompanyDialog = true"
                  />
                </v-window-item>

                <!-- Услуги компании -->
                <v-window-item value="services">
                  <CompanyServicesTab
                      :company="company"
                      @service-added="loadCompanyData"
                      @service-updated="loadCompanyData"
                      @service-deleted="loadCompanyData"
                      @service-discount-added="loadCompanyData"
                  />
                </v-window-item>

                <!-- Заявки на услуги -->
                <v-window-item value="requests">
                  <CompanyRequestsTab
                      :company="company"
                      @request-updated="loadCompanyData"
                  />
                </v-window-item>

                <!-- Скидки на услуги -->
                <v-window-item value="discounts">
                  <CompanyDiscountsTab
                      :company="company"
                      @discount-added="loadDiscounts"
                      @discount-updated="loadDiscounts"
                      @discount-deleted="loadDiscounts"
                  />
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Диалог удаления компании -->
    <DeleteConfirmationDialog
        :dialog="deleteCompanyDialog"
        @update:dialog="deleteCompanyDialog = $event"
        :loading="deleteLoading"
        title="Удаление компании"
        message="Вы уверены, что хотите удалить компанию? <br><strong>Это действие нельзя отменить. Все данные компании (услуги, скидки) будут удалены.</strong>"
        @close="deleteCompanyDialog = false"
        @confirm="confirmDeleteCompany"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import apiClient from '@/api'

// Компоненты
import SuccessNotification from '@/components/ui/SuccessNotification.vue'
import DeleteConfirmationDialog from '@/components/ui/DeleteConfirmationDialog.vue'
import CompanyInfoTab from '@/components/company/CompanyInfoTab.vue'
import CompanyServicesTab from '@/components/company/CompanyServicesTab.vue'
import CompanyRequestsTab from '@/components/company/CompanyRequestsTab.vue'
import CompanyDiscountsTab from '@/components/company/CompanyDiscountsTab.vue'

const authStore = useAuthStore()
const router = useRouter()

// Состояния
const isLoading = ref(false)
const company = ref({})
const activeTab = ref('info')
const deleteCompanyDialog = ref(false)
const deleteLoading = ref(false)

// Уведомления
const successSnackbar = reactive({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// Вспомогательные функции
const showSuccessMessage = (message, type = 'success') => {
  successSnackbar.text = message
  successSnackbar.color = type
  successSnackbar.icon = type === 'success' ? 'mdi-check-circle' : 'mdi-alert-circle'
  successSnackbar.show = true
}

// Основные методы
const loadCompanyData = async () => {
  if (!authStore.hasCompany) return

  isLoading.value = true
  try {
    const response = await apiClient.get('companies/my/')
    company.value = response.data
  } catch (error) {
    console.error('Error loading company data:', error)
    showSuccessMessage('Ошибка загрузки данных компании', 'error')
  } finally {
    isLoading.value = false
  }
}

const loadDiscounts = async () => {
  // Загрузка скидок выполняется в соответствующем компоненте
  // Здесь просто обновляем данные компании, если нужно
  await loadCompanyData()
}

const confirmDeleteCompany = async () => {
  deleteLoading.value = true
  try {
    await apiClient.delete('companies/destroy_my/')

    // Обновляем данные пользователя
    await authStore.fetchUser()

    deleteCompanyDialog.value = false
    showSuccessMessage('Компания успешно удалена!')

    // Перенаправляем на главную страницу
    router.push('/')
  } catch (error) {
    console.error('Error deleting company:', error)
    showSuccessMessage('Ошибка удаления компании', 'error')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(async () => {
  if (authStore.hasCompany) {
    await loadCompanyData()
  }
})
</script>

<style scoped>
/* Стили для вкладок */
:deep(.v-tab) {
  text-transform: none;
  font-weight: 500;
}

:deep(.v-tab--selected) {
  background-color: rgba(25, 118, 210, 0.08);
}

/* Стили для окон вкладок */
:deep(.v-window-item) {
  padding: 24px;
}
</style>