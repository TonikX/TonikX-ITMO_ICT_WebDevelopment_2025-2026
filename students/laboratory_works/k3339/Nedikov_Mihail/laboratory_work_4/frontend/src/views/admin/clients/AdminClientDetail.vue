<template>
  <div>
    <!-- Навигация -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn @click="$router.push('/admin/clients')" color="secondary">
          <v-icon left>mdi-arrow-left</v-icon>
          К списку клиентов
        </v-btn>
      </v-col>
    </v-row>

    <!-- Загрузка -->
    <v-row v-if="loading">
      <v-col cols="12">
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
        <div class="text-center mt-4">Загрузка данных клиента...</div>
      </v-col>
    </v-row>

    <!-- Основная информация -->
    <v-row v-else-if="client">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="headline">
            {{ client.company_name }}
            <v-chip class="ml-4" :color="client.is_active ? 'green' : 'red'" dark>
              {{ client.is_active ? 'Активен' : 'Неактивен' }}
            </v-chip>
          </v-card-title>

          <v-card-subtitle>
            Клиент #{{ client.id }} • ИНН: {{ client.inn }}
          </v-card-subtitle>

          <v-divider class="my-4"></v-divider>

          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Название компании</v-list-item-title>
                  <v-list-item-subtitle class="text-h6">
                    {{ client.company_name }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>ИНН</v-list-item-title>
                  <v-list-item-subtitle class="text-h6">
                    {{ client.inn }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>{{ client.email || '—' }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Телефон</v-list-item-title>
                  <v-list-item-subtitle>{{ client.phone || '—' }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Контактное лицо</v-list-item-title>
                  <v-list-item-subtitle>{{ client.contact_person || '—' }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Адрес</v-list-item-title>
                  <v-list-item-subtitle>{{ client.address || '—' }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Статус</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip :color="client.is_active ? 'green' : 'red'" dark small>
                      {{ client.is_active ? 'Активен' : 'Неактивен' }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-col>

              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-title>Дата регистрации</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDateTime(client.created_at) }}</v-list-item-subtitle>
                </v-list-item>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Боковая панель -->
      <v-col cols="12" md="4">
        <!-- Быстрые действия -->
        <v-card class="mb-4">
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                  @click="copyClientInfo"
                  prepend-icon="mdi-content-copy"
              >
                <v-list-item-title>Копировать информацию</v-list-item-title>
              </v-list-item>

              <v-list-item
                  @click="showClientLeases"
                  prepend-icon="mdi-file-document"
              >
                <v-list-item-title>История аренд</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Статистика -->
        <v-card>
          <v-card-title>Статистика клиента</v-card-title>
          <v-card-text>
            <v-alert type="info">
              <div class="text-center">
                <div class="text-h6">Нет данных</div>
              </div>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Ошибка -->
    <v-alert v-else-if="error" type="error">
      {{ errorMessage }}
      <v-btn @click="fetchClient" class="mt-2" color="error">Попробовать снова</v-btn>
    </v-alert>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminClientDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      client: null,
      loading: true,
      error: false,
      errorMessage: ''
    }
  },
  computed: {
    clientId() {
      return parseInt(this.id)
    }
  },
  methods: {
    async fetchClient() {
      try {
        this.loading = true
        this.error = false

        const response = await axios.get(`admin/clients/${this.clientId}/`)
        this.client = response.data.client
        console.log('Данные клиента загружены:', this.client)

      } catch (error) {
        console.error('Ошибка загрузки клиента:', error)
        this.error = true
        this.errorMessage = error.response?.data?.detail || 'Не удалось загрузить данные клиента'
      } finally {
        this.loading = false
      }
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '—'
      return new Date(dateTimeString).toLocaleString('ru-RU')
    },
    copyClientInfo() {
      const text = `Клиент #${this.client.id}
Компания: ${this.client.company_name}
ИНН: ${this.client.inn}
Email: ${this.client.email || 'не указан'}
Телефон: ${this.client.phone || 'не указан'}
Контактное лицо: ${this.client.contact_person || 'не указано'}
Адрес: ${this.client.address || 'не указан'}
Статус: ${this.client.is_active ? 'Активен' : 'Неактивен'}
Дата регистрации: ${this.formatDateTime(this.client.created_at)}`

      navigator.clipboard.writeText(text)
          .then(() => {
            alert('Информация скопирована в буфер обмена')
          })
          .catch(err => {
            console.error('Ошибка копирования:', err)
          })
    },
  },
  mounted() {
    this.fetchClient()
  },
  watch: {
    id() {
      this.fetchClient()
    }
  }
}
</script>