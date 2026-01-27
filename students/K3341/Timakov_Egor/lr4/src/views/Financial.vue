<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span class="text-h5">Финансовые записи</span>
            <v-btn color="primary" @click="openDialog()">
              <v-icon start>mdi-plus</v-icon>
              Добавить запись
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-select
                    v-model="typeFilter"
                    :items="transactionTypes"
                    item-value="value"
                    item-title="title"
                    label="Тип операции"
                    variant="outlined"
                    @change="loadFinancial"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                    v-model="startDate"
                    label="Начальная дата"
                    type="date"
                    variant="outlined"
                    @change="loadFinancial"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                    v-model="endDate"
                    label="Конечная дата"
                    type="date"
                    variant="outlined"
                    @change="loadFinancial"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-btn color="info" @click="loadSummary">Сводка</v-btn>
              </v-col>
            </v-row>

            <v-data-table
                :headers="headers"
                :items="financial"
                :loading="loading"
                item-key="id"
            >
              <template v-slot:item.transaction_type_display="{ item }">
                <v-chip :color="item.transaction_type === 'income' ? 'green' : 'red'">
                  {{ item.transaction_type_display }}
                </v-chip>
              </template>
              <template v-slot:item.amount="{ item }">
                {{ formatCurrency(item.amount) }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn icon="mdi-pencil" size="small" @click="openDialog(item)"></v-btn>
                <v-btn icon="mdi-delete" size="small" color="error" @click="deleteItem(item)"></v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>{{ editingItem ? 'Редактировать' : 'Добавить' }} запись</v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
                v-model="form.date"
                label="Дата"
                type="date"
                variant="outlined"
                required
            ></v-text-field>
            <v-select
                v-model="form.transaction_type"
                :items="transactionTypes"
                item-value="value"
                item-title="title"
                label="Тип операции"
                variant="outlined"
                required
            ></v-select>
            <v-select
                v-model="form.category"
                :items="categories"
                item-value="value"
                item-title="title"
                label="Категория"
                variant="outlined"
                required
            ></v-select>
            <v-text-field
                v-model="form.amount"
                label="Сумма"
                type="number"
                variant="outlined"
                required
            ></v-text-field>
            <v-textarea
                v-model="form.description"
                label="Описание"
                variant="outlined"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="handleDialogCancel">Отмена</v-btn>
          <v-btn color="primary" @click="saveItem">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог сводки -->
    <v-dialog v-model="summaryDialog" max-width="600">
      <v-card>
        <v-card-title>Финансовая сводка</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-title>Общий доход</v-list-item-title>
              <v-list-item-subtitle>{{ formatCurrency(summary.total_income) }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Общий расход</v-list-item-title>
              <v-list-item-subtitle>{{ formatCurrency(summary.total_expense) }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Баланс</v-list-item-title>
              <v-list-item-subtitle>{{ formatCurrency(summary.balance) }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="summaryDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { financialApi } from '../services/api'

export default {
  name: 'Financial',
  setup() {
    const financial = ref([]) // Список финансовых записей
    const loading = ref(false)
    const typeFilter = ref('')
    const startDate = ref('')
    const endDate = ref('')
    const dialog = ref(false)
    const summaryDialog = ref(false)
    const editingItem = ref(null)
    const summary = reactive({
      total_income: 0,
      total_expense: 0,
      balance: 0
    })
    const form = reactive({
      date: '',
      transaction_type: '',
      category: '',
      amount: '',
      description: ''
    })

    const transactionTypes = [
      { title: 'Доход', value: 'income' },
      { title: 'Расход', value: 'expense' }
    ]

    const categories = [
      { title: 'Продажа книг', value: 'book_sales' },
      { title: 'Услуги печати', value: 'printing_services' },
      { title: 'Зарплата', value: 'salary' },
      { title: 'Материалы', value: 'materials' },
      { title: 'Оборудование', value: 'equipment' },
      { title: 'Аренда', value: 'rent' },
      { title: 'Коммунальные услуги', value: 'utilities' },
      { title: 'Прочее', value: 'other' }
    ]

    const headers = [
      { title: 'Дата', key: 'date' },
      { title: 'Тип', key: 'transaction_type_display' },
      { title: 'Категория', key: 'category_display' },
      { title: 'Сумма', key: 'amount' },
      { title: 'Описание', key: 'description' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const formatCurrency = (value) => {
      return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
    }

    const resetForm = () => {
      Object.assign(form, {
        date: '',
        transaction_type: '',
        category: '',
        amount: '',
        description: ''
      })
    }

    const loadFinancial = async () => {
      loading.value = true
      try {
        const params = {
          type: typeFilter.value,
          start_date: startDate.value,
          end_date: endDate.value
        }
        const response = await financialApi.getAll(params)
        financial.value = response.data.results || []
      } catch (error) {
        console.error('Ошибка загрузки финансов:', error)
      } finally {
        loading.value = false
      }
    }

    const loadSummary = async () => {
      try {
        const params = {
          start_date: startDate.value,
          end_date: endDate.value
        }
        const response = await financialApi.getSummary(params)
        Object.assign(summary, response.data || {})
        summaryDialog.value = true
      } catch (error) {
        console.error('Ошибка загрузки сводки:', error)
      }
    }

    const openDialog = (item = null) => {
      editingItem.value = item || null
      Object.assign(form, {
        date: item?.date || '',
        transaction_type: item?.transaction_type || '',
        category: item?.category || '',
        amount: item?.amount || '',
        description: item?.description || ''
      })
      dialog.value = true
    }

    const handleDialogCancel = () => {
      dialog.value = false
      resetForm()
    }

    const saveItem = async () => {
      try {
        if (editingItem.value) {
          await financialApi.update(editingItem.value.id, { ...form })
        } else {
          await financialApi.create({ ...form })
        }
        dialog.value = false
        resetForm()
        loadFinancial()
      } catch (error) {
        console.error('Ошибка сохранения:', error)
      }
    }

    const deleteItem = async (item) => {
      if (confirm('Удалить запись?')) {
        try {
          await financialApi.delete(item.id)
          loadFinancial()
        } catch (error) {
          console.error('Ошибка удаления:', error)
        }
      }
    }

    onMounted(loadFinancial)

    return {
      financial,
      loading,
      typeFilter,
      startDate,
      endDate,
      dialog,
      summaryDialog,
      editingItem,
      summary,
      form,
      transactionTypes,
      categories,
      headers,
      formatCurrency,
      loadFinancial,
      loadSummary,
      openDialog,
      handleDialogCancel,
      saveItem,
      deleteItem
    }
  }
}
</script>