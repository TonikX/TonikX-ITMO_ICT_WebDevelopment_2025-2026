<template>
  <v-container class="my-8">
    <h1 class="text-h4 text-center mb-6">Заявки</h1>

    <v-row v-if="orders.length">
      <v-col
          v-for="order in orders"
          :key="order.id"
          cols="12"
          md="6"
      >
        <v-card class="pa-4">
          <p><b>ID:</b> {{ order.id }}</p>
          <p><b>Пользователь:</b> {{ order.user_email }}</p>
          <p><b>Услуга:</b> {{ order.service_name }}</p>
          <p><b>Статус:</b> 
            <v-chip 
              :color="getStatusColor(order.status)" 
              size="small"
              variant="tonal"
            >
              {{ getStatusLabel(order.status) }}
            </v-chip>
          </p>

          <v-btn
              class="mr-2"
              size="small"
              @click="loadHistory(order)"
          >
            История
          </v-btn>

          <v-btn
              size="small"
              color="primary"
              @click="openStatusDialog(order)"
          >
            Изменить статус
          </v-btn>

          <v-btn
              size="small"
              color="secondary"
              @click="() => { selectedOrder = order; commentContent=''; isVisibleToUser=true; commentDialog=true }"
          >
            Оставить комментарий
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12" class="text-center">
        <p>Данные недоступны</p>
      </v-col>
    </v-row>

    <!-- История -->
    <v-dialog v-model="historyDialog" max-width="600">
      <v-card class="pa-4">
        <h3 class="mb-4">История статусов</h3>
        <div v-if="history.length">
          <div v-for="item in history" :key="item.id" class="mb-3 pa-3 bg-grey-lighten-5 rounded">
            <div class="font-weight-medium">
              {{ getStatusLabel(item.old_status) }} → {{ getStatusLabel(item.new_status) }}
            </div>
            <div class="text-caption text-grey">
              {{ new Date(item.changed_at).toLocaleString() }}
            </div>
            <div v-if="item.comment" class="mt-1 text-body-2">
              💬 {{ item.comment }}
            </div>
          </div>
        </div>
        <div v-else class="text-center py-4">
          История пуста
        </div>
        <v-btn class="mt-4" @click="historyDialog = false">Закрыть</v-btn>
      </v-card>
    </v-dialog>

    <!-- Изменение статуса -->
    <v-dialog v-model="statusDialog" max-width="400">
      <v-card class="pa-4">
        <v-select
          v-model="newStatus"
          :items="statusOptions"
          item-title="label"
          item-value="value"
          label="Новый статус"
          :rules="[v => !!v || 'Выберите статус']"
          variant="outlined"
        />
        <v-textarea
          v-model="comment"
          label="Комментарий (опционально)"
          rows="2"
          variant="outlined"
          class="mt-2"
        />
        <v-card-actions class="pt-4">
          <v-btn @click="statusDialog = false">Отмена</v-btn>
          <v-spacer/>
          <v-btn 
            color="primary" 
            @click="changeStatus"
            :loading="loading"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Добавление комментария -->
    <v-dialog v-model="commentDialog" max-width="400">
      <v-card class="pa-4">
        <h3 class="mb-4">Комментарий к заявке #{{ selectedOrder?.id }}</h3>

        <v-textarea
            v-model="commentContent"
            label="Комментарий"
            rows="3"
            variant="outlined"
            :rules="[v => !!v || 'Комментарий не может быть пустым']"
        />

        <v-checkbox
            v-model="isVisibleToUser"
            label="Виден пользователю"
            color="primary"
        />

        <v-card-actions class="pt-2">
          <v-btn @click="commentDialog = false">Отмена</v-btn>
          <v-spacer/>
          <v-btn 
            color="primary" 
            @click="addComment"
            :loading="loading"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

// Глобальная настройка CSRF для всех запросов Axios
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default {
  name: 'AdminOrdersView',

  data() {
    return {
      orders: [],
      history: [],
      selectedOrder: null,

      historyDialog: false,
      statusDialog: false,
      commentDialog: false,

      // Допустимые статусы — ДОЛЖНЫ СОВПАДАТЬ С МОДЕЛЬЮ DJANGO!
      statusOptions: [
        { value: 'new', label: 'Новая' },
        { value: 'in_progress', label: 'В работе' },
        { value: 'completed', label: 'Завершена' },
        { value: 'cancelled', label: 'Отменена' }
      ],
      newStatus: '',
      comment: '',

      commentContent: '',
      isVisibleToUser: true,
      
      loading: false
    }
  },

  async mounted() {
    try {
      const res = await axios.get('/api/admin/orders/')
      this.orders = res.data.filter(o => o.status !== 'cancelled')
    } catch (error) {
      console.error('Ошибка загрузки заявок:', error.response?.data || error.message)
      this.orders = []
    }
  },

  methods: {
    getStatusLabel(value) {
      const option = this.statusOptions.find(opt => opt.value === value)
      return option ? option.label : value
    },
    
    getStatusColor(status) {
      const colors = {
        new: 'blue',
        in_progress: 'orange',
        completed: 'green',
        cancelled: 'red'
      }
      return colors[status] || 'grey'
    },

    async loadHistory(order) {
      try {
        const res = await axios.get(`/api/admin/orders/${order.id}/history/`)
        this.history = res.data
        this.historyDialog = true
      } catch (error) {
        console.error('Ошибка загрузки истории:', error.response?.data || error.message)
        this.history = []
        this.historyDialog = true
      }
    },

    openStatusDialog(order) {
      this.selectedOrder = order
      this.newStatus = order.status // текущий статус
      this.comment = ''
      this.statusDialog = true
    },

    async changeStatus() {
      if (!this.newStatus) {
        alert('Выберите статус')
        return
      }

      this.loading = true
      try {
        await axios.patch(
            `/api/admin/orders/${this.selectedOrder.id}/status/`,
            { 
              status: this.newStatus, 
              comment: this.comment.trim() || null 
            }
        )
        
        // Обновляем статус локально без перезагрузки
        const index = this.orders.findIndex(o => o.id === this.selectedOrder.id)
        if (index !== -1) {
          this.orders[index].status = this.newStatus
        }
        
        this.statusDialog = false
        this.$toast.success('Статус успешно изменён')
      } catch (error) {
        console.error('Ошибка изменения статуса:', error.response?.data)
        
        // Показываем детали ошибки пользователю
        const errorMsg = error.response?.data?.status?.[0] || 
                         error.response?.data?.detail || 
                         'Не удалось изменить статус'
        
        alert(`Ошибка: ${errorMsg}`)
      } finally {
        this.loading = false
      }
    },

    async addComment() {
      if (!this.commentContent.trim()) {
        alert('Комментарий не может быть пустым')
        return
      }

      this.loading = true
      try {
        await axios.post('/api/admin/comments/', {
          order: this.selectedOrder.id,
          content: this.commentContent.trim(),
          is_visible_to_user: this.isVisibleToUser
        })

        this.commentDialog = false
        this.$toast.success('Комментарий добавлен')
      } catch (error) {
        console.error('Ошибка добавления комментария:', error.response?.data)
        alert('Ошибка при добавлении комментария: ' + (error.response?.data?.detail || 'неизвестная ошибка'))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>