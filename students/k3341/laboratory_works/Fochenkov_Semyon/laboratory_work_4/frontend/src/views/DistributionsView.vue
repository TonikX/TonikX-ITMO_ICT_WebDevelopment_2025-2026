<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Распределения</span>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
              Создать распределение
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="distributions"
              :loading="loading"
              :items-per-page="20"
              :server-items-length="totalCount"
              @update:options="loadDistributions"
            >
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  @click="openEditDialog(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                />
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ editingItem ? 'Редактировать распределение' : 'Создать распределение' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-select
              v-model="form.post_office"
              :items="postOfficesForSelect"
              item-title="display"
              item-value="id"
              label="Почтовое отделение"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-select
              v-model="form.newspaper"
              :items="newspapers"
              item-title="title"
              item-value="id"
              label="Газета"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-select
              v-model="form.printing_house"
              :items="printingHouses"
              item-title="name"
              item-value="id"
              label="Типография"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.quantity"
              label="Количество"
              type="number"
              :rules="[rules.required, rules.positive]"
              variant="outlined"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="save" :loading="saving">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить это распределение?
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="error" @click="deleteItem" :loading="deleting">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import api from '@/services/api'
import type { Distribution, Newspaper, PrintingHouse, PostOffice, DistributionForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false },
  { title: 'Почтовое отделение', key: 'post_office_number', sortable: false },
  { title: 'Газета', key: 'newspaper_title', sortable: false },
  { title: 'Типография', key: 'printing_house_name', sortable: false },
  { title: 'Количество', key: 'quantity', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false },
]

const distributions = ref<Distribution[]>([])
const newspapers = ref<Newspaper[]>([])
const printingHouses = ref<PrintingHouse[]>([])
const postOffices = ref<PostOffice[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<Distribution | null>(null)
const itemToDelete = ref<Distribution | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<DistributionForm>({
  post_office: null,
  newspaper: null,
  printing_house: null,
  quantity: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'Обязательное поле') as ValidationRule,
  positive: ((v: string | number | null | undefined) => {
    const num = typeof v === 'string' ? parseInt(v) : v
    return (num && num > 0) || 'Значение должно быть положительным'
  }) as ValidationRule,
}

const postOfficesForSelect = computed(() => {
  return postOffices.value.map(po => ({
    id: po.id,
    display: `${po.number} - ${po.address}`,
  }))
})

async function loadDistributions(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getDistributions(params)
    distributions.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Ошибка загрузки распределений')
  } finally {
    loading.value = false
  }
}

async function loadSelectData() {
  try {
    const [newspapersData, printingHousesData, postOfficesData] = await Promise.all([
      api.getNewspapers({ page_size: 1000 }),
      api.getPrintingHouses({ page_size: 1000 }),
      api.getPostOffices({ page_size: 1000 }),
    ])

    newspapers.value = newspapersData.results || []
    printingHouses.value = printingHousesData.results || []
    postOffices.value = postOfficesData.results || []
  } catch {
    console.error('Ошибка загрузки данных для выбора')
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: Distribution) {
  editingItem.value = item
  form.post_office = item.post_office
  form.newspaper = item.newspaper
  form.printing_house = item.printing_house
  form.quantity = item.quantity.toString()
  dialog.value = true
}

function resetForm() {
  form.post_office = null
  form.newspaper = null
  form.printing_house = null
  form.quantity = ''
}

function closeDialog() {
  dialog.value = false
  editingItem.value = null
  resetForm()
}

async function save() {
  if (!formRef.value) return
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = {
      post_office: form.post_office!,
      newspaper: form.newspaper!,
      printing_house: form.printing_house!,
      quantity: parseInt(form.quantity),
    }

    if (editingItem.value) {
      await api.updateDistribution(editingItem.value.id, data)
    } else {
      await api.createDistribution(data)
    }
    closeDialog()
    loadDistributions()
  } catch {
    console.error('Ошибка сохранения')
  } finally {
    saving.value = false
  }
}

function confirmDelete(item: Distribution) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deleteDistribution(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadDistributions()
  } catch {
    console.error('Ошибка удаления')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadDistributions({ page: 1, itemsPerPage: 20 })
  loadSelectData()
})
</script>

