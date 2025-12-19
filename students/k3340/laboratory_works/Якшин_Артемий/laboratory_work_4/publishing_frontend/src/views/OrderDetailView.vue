<template>
  <div class="order-detail-view">
    <v-btn class="mb-4" variant="text" :to="{ name: 'orders' }">
      <v-icon left>mdi-arrow-left</v-icon>
      Назад к списку
    </v-btn>

    <v-skeleton-loader v-if="loading" type="article, actions"></v-skeleton-loader>

    <template v-else-if="order">
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title class="d-flex align-center justify-space-between">
              <span>
                <v-icon class="mr-2">mdi-cart</v-icon>
                Заказ {{ order.order_number }}
              </span>
              <v-chip :color="getStatusColor(order.status)" label>
                {{ getStatusLabel(order.status) }}
              </v-chip>
            </v-card-title>

            <v-card-text>
              <v-row>
                <v-col cols="6" md="4">
                  <div class="text-caption text-medium-emphasis">Дата заказа</div>
                  <div class="text-h6">{{ formatDate(order.order_date) }}</div>
                </v-col>
                <v-col cols="6" md="4">
                  <div class="text-caption text-medium-emphasis">Общая сумма</div>
                  <div class="text-h6">{{ formatPrice(order.total_amount) }}</div>
                </v-col>
                <v-col cols="6" md="4">
                  <div class="text-caption text-medium-emphasis">Рассчитанная сумма</div>
                  <div class="text-h6">{{ formatPrice(order.calculated_total) }}</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Order Items -->
          <v-card class="mt-4">
            <v-card-title class="d-flex align-center justify-space-between">
              <span>
                <v-icon class="mr-2">mdi-format-list-bulleted</v-icon>
                Позиции заказа
              </span>
              <v-btn size="small" color="primary" variant="tonal" @click="openItemDialog">
                <v-icon>mdi-plus</v-icon>
                Добавить
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="itemHeaders"
                :items="order.items"
                density="compact"
                class="elevation-0"
              >
                <template v-slot:item.unit_price="{ item }">
                  {{ formatPrice(item.unit_price) }}
                </template>

                <template v-slot:item.subtotal="{ item }">
                  {{ formatPrice(item.subtotal) }}
                </template>

                <template v-slot:item.actions="{ item }">
                  <v-btn icon="mdi-delete" size="x-small" variant="text" color="error" 
                         @click="deleteOrderItem(item.id)"></v-btn>
                </template>

                <template v-slot:no-data>
                  <div class="text-center pa-4 text-medium-emphasis">
                    Позиции не добавлены
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <!-- Customer Info -->
          <v-card>
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-account-tie</v-icon>
              Заказчик
            </v-card-title>
            <v-card-text v-if="order.customer_details">
              <div class="mb-3">
                <div class="text-caption text-medium-emphasis">Имя</div>
                <div class="font-weight-medium">{{ order.customer_details.name }}</div>
              </div>
              <div class="mb-3" v-if="order.customer_details.company_name">
                <div class="text-caption text-medium-emphasis">Компания</div>
                <div>{{ order.customer_details.company_name }}</div>
              </div>
              <div class="mb-3">
                <div class="text-caption text-medium-emphasis">Email</div>
                <div>{{ order.customer_details.email }}</div>
              </div>
              <div class="mb-3">
                <div class="text-caption text-medium-emphasis">Телефон</div>
                <div>{{ order.customer_details.phone }}</div>
              </div>
              <div v-if="order.customer_details.address">
                <div class="text-caption text-medium-emphasis">Адрес</div>
                <div>{{ order.customer_details.address }}</div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- Add Item Dialog -->
    <v-dialog v-model="itemDialog" max-width="500">
      <v-card>
        <v-card-title>Добавить позицию</v-card-title>
        <v-card-text>
          <v-form ref="itemForm" v-model="itemFormValid">
            <v-select
              v-model="itemFormData.book"
              :items="availableBooks"
              item-title="title"
              item-value="id"
              label="Книга"
              :rules="[rules.required]"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :subtitle="formatPrice(item.raw.cover_price)"></v-list-item>
              </template>
            </v-select>
            <v-text-field
              v-model.number="itemFormData.quantity"
              label="Количество"
              type="number"
              :rules="[rules.required, rules.positive]"
            ></v-text-field>
            <v-text-field
              v-model.number="itemFormData.unit_price"
              label="Цена за единицу"
              type="number"
              step="0.01"
              prefix="₽"
              :rules="[rules.required, rules.positive]"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="itemDialog = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!itemFormValid" @click="addItem">
            Добавить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ordersApi, booksApi, orderItemsApi } from '@/services/api'

const route = useRoute()
const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const order = ref(null)
const allBooks = ref([])

const itemDialog = ref(false)
const itemForm = ref(null)
const itemFormValid = ref(false)

const itemFormData = reactive({
  book: null,
  quantity: 1,
  unit_price: null
})

const itemHeaders = [
  { title: 'Книга', key: 'book_title' },
  { title: 'Кол-во', key: 'quantity', width: '100px' },
  { title: 'Цена', key: 'unit_price', width: '120px' },
  { title: 'Сумма', key: 'subtotal', width: '120px' },
  { title: '', key: 'actions', sortable: false, width: '60px' }
]

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  positive: (v) => v > 0 || 'Должно быть больше 0'
}

const availableBooks = computed(() => {
  const existingBookIds = order.value?.items?.map(i => i.book) || []
  return allBooks.value.filter(b => !existingBookIds.includes(b.id))
})

const selectedBook = computed(() => {
  return allBooks.value.find(b => b.id === itemFormData.book)
})

watch(() => itemFormData.book, (newVal) => {
  if (newVal && selectedBook.value) {
    itemFormData.unit_price = parseFloat(selectedBook.value.cover_price)
  }
})

const getStatusColor = (status) => {
  const colors = { PENDING: 'warning', PROCESSING: 'info', COMPLETED: 'success', CANCELLED: 'error' }
  return colors[status] || 'grey'
}

const getStatusLabel = (status) => {
  const labels = { PENDING: 'Ожидает', PROCESSING: 'В обработке', COMPLETED: 'Завершён', CANCELLED: 'Отменён' }
  return labels[status] || status
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(price)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchOrder = async () => {
  loading.value = true
  try {
    const response = await ordersApi.getOne(route.params.id)
    order.value = response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки заказа', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchBooks = async () => {
  try {
    const response = await booksApi.getAll()
    allBooks.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const openItemDialog = () => {
  itemFormData.book = null
  itemFormData.quantity = 1
  itemFormData.unit_price = null
  itemDialog.value = true
}

const addItem = async () => {
  const { valid } = await itemForm.value.validate()
  if (!valid) return

  saving.value = true
  try {
    await orderItemsApi.create({
      order: order.value.id,
      book: itemFormData.book,
      quantity: itemFormData.quantity,
      unit_price: itemFormData.unit_price
    })
    showSnackbar('Позиция добавлена', 'success')
    itemDialog.value = false
    fetchOrder()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка добавления'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const deleteOrderItem = async (id) => {
  try {
    await orderItemsApi.delete(id)
    showSnackbar('Позиция удалена', 'success')
    fetchOrder()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  }
}

onMounted(() => {
  fetchOrder()
  fetchBooks()
})
</script>

<style scoped>
.order-detail-view {
  max-width: 1200px;
  margin: 0 auto;
}
</style>

