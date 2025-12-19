<template>
  <div class="orders-view">
    <v-row class="mb-4">
      <v-col cols="12" class="d-flex justify-space-between align-center flex-wrap">
        <h1 class="page-title">
          <v-icon class="mr-2">mdi-cart</v-icon>
          Заказы
        </h1>
        <v-btn color="primary" @click="openDialog()">
          <v-icon left>mdi-plus</v-icon>
          Создать заказ
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title class="d-flex flex-wrap gap-4">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
          density="compact"
          style="max-width: 300px"
        ></v-text-field>

        <v-select
          v-model="statusFilter"
          :items="statusOptions"
          label="Статус"
          clearable
          hide-details
          density="compact"
          style="max-width: 200px"
        ></v-select>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="filteredOrders"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" label>
            {{ getStatusLabel(item.status) }}
          </v-chip>
        </template>

        <template v-slot:item.total_amount="{ item }">
          {{ formatPrice(item.total_amount) }}
        </template>

        <template v-slot:item.order_date="{ item }">
          {{ formatDate(item.order_date) }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-eye" size="small" variant="text" :to="{ name: 'order-detail', params: { id: item.id } }"></v-btn>
          <v-btn icon="mdi-pencil" size="small" variant="text" @click="openDialog(item)"></v-btn>
          <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="confirmDelete(item)"></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="48" color="grey">mdi-cart-off</v-icon>
            <p class="mt-2 text-medium-emphasis">Заказы не найдены</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">{{ editingItem ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ editingItem ? 'Редактировать заказ' : 'Новый заказ' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.order_number"
                  label="Номер заказа"
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.status"
                  :items="statusOptions"
                  label="Статус"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="formData.customer"
                  :items="customers"
                  item-title="name"
                  item-value="id"
                  label="Заказчик"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model.number="formData.total_amount"
                  label="Общая сумма"
                  type="number"
                  step="0.01"
                  prefix="₽"
                  :rules="[rules.required, rules.positive]"
                  :hint="editingItem ? 'Рассчитанная сумма: ' + formatPrice(editingItem.calculated_total) : ''"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!formValid" @click="saveItem">
            {{ editingItem ? 'Сохранить' : 'Создать' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить заказ 
          <strong>{{ itemToDelete?.order_number }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteItem">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { ordersApi, customersApi } from '@/services/api'

const showSnackbar = inject('showSnackbar')

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const orders = ref([])
const customers = ref([])
const search = ref('')
const statusFilter = ref(null)

const dialog = ref(false)
const deleteDialog = ref(false)
const form = ref(null)
const formValid = ref(false)
const editingItem = ref(null)
const itemToDelete = ref(null)

const headers = [
  { title: 'ID', key: 'id', width: '80px' },
  { title: '№ Заказа', key: 'order_number', width: '140px' },
  { title: 'Заказчик', key: 'customer_name' },
  { title: 'Статус', key: 'status', width: '160px' },
  { title: 'Сумма', key: 'total_amount', width: '130px' },
  { title: 'Позиций', key: 'items_count', width: '100px' },
  { title: 'Дата', key: 'order_date', width: '140px' },
  { title: 'Действия', key: 'actions', sortable: false, width: '140px' }
]

const statusOptions = [
  { title: 'Ожидает', value: 'PENDING' },
  { title: 'В обработке', value: 'PROCESSING' },
  { title: 'Завершён', value: 'COMPLETED' },
  { title: 'Отменён', value: 'CANCELLED' }
]

const formData = reactive({
  order_number: '',
  customer: null,
  status: 'PENDING',
  total_amount: null
})

const rules = {
  required: (v) => !!v || v === 0 || 'Обязательное поле',
  positive: (v) => v >= 0 || 'Не может быть отрицательным'
}

const filteredOrders = computed(() => {
  if (!statusFilter.value) return orders.value
  return orders.value.filter(o => o.status === statusFilter.value)
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

const fetchOrders = async () => {
  loading.value = true
  try {
    const response = await ordersApi.getAll()
    orders.value = response.data.results || response.data
  } catch (error) {
    showSnackbar('Ошибка загрузки заказов', 'error')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const fetchCustomers = async () => {
  try {
    const response = await customersApi.getAll()
    customers.value = response.data.results || response.data
  } catch (error) {
    console.error(error)
  }
}

const openDialog = (item = null) => {
  editingItem.value = item
  if (item) {
    Object.assign(formData, {
      order_number: item.order_number,
      customer: item.customer,
      status: item.status,
      total_amount: item.total_amount
    })
  } else {
    Object.assign(formData, {
      order_number: `ORD-${Date.now()}`,
      customer: null,
      status: 'PENDING',
      total_amount: 0
    })
  }
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  editingItem.value = null
  form.value?.reset()
}

const saveItem = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  saving.value = true
  try {
    if (editingItem.value) {
      await ordersApi.update(editingItem.value.id, formData)
      showSnackbar('Заказ обновлён', 'success')
    } else {
      await ordersApi.create(formData)
      showSnackbar('Заказ создан', 'success')
    }
    closeDialog()
    fetchOrders()
  } catch (error) {
    const errorMsg = error.response?.data?.detail || 
                     Object.values(error.response?.data || {}).flat().join('. ') ||
                     'Ошибка сохранения'
    showSnackbar(errorMsg, 'error')
  } finally {
    saving.value = false
  }
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  deleteDialog.value = true
}

const deleteItem = async () => {
  deleting.value = true
  try {
    await ordersApi.delete(itemToDelete.value.id)
    showSnackbar('Заказ удалён', 'success')
    deleteDialog.value = false
    fetchOrders()
  } catch (error) {
    showSnackbar('Ошибка удаления', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchOrders()
  fetchCustomers()
})
</script>

<style scoped>
.orders-view {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: rgb(var(--v-theme-on-background));
}
</style>

