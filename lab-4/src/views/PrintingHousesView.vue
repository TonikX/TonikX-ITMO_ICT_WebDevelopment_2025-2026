<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Типографии</span>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
              Создать типографию
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="printingHouses"
              :loading="loading"
              :items-per-page="20"
              :server-items-length="totalCount"
              @update:options="loadPrintingHouses"
            >
              <template v-slot:item.is_active="{ item }">
                <v-chip :color="item.is_active ? 'success' : 'error'" size="small">
                  {{ item.is_active ? 'Активна' : 'Неактивна' }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewDetails(item)"
                />
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
          {{ editingItem ? 'Редактировать типографию' : 'Создать типографию' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.name"
              label="Название"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.address"
              label="Адрес"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-switch
              v-model="form.is_active"
              label="Активна"
              color="success"
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

    <v-dialog v-model="detailsDialog" max-width="800px">
      <v-card v-if="selectedItem">
        <v-card-title>Детали типографии</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <p><strong>Название:</strong> {{ selectedItem.name }}</p>
              <p><strong>Адрес:</strong> {{ selectedItem.address }}</p>
              <p><strong>Статус:</strong>
                <v-chip :color="selectedItem.is_active ? 'success' : 'error'" size="small">
                  {{ selectedItem.is_active ? 'Активна' : 'Неактивна' }}
                </v-chip>
              </p>
            </v-col>
          </v-row>
          <v-divider class="my-4" />
          <div v-if="fullDetails">
            <h3 class="mb-2">Тиражи</h3>
            <v-list v-if="fullDetails.printing_runs?.length">
              <v-list-item
                v-for="run in fullDetails.printing_runs"
                :key="run.id"
              >
                {{ run.newspaper.title }} - тираж: {{ run.circulation }}
              </v-list-item>
            </v-list>
            <p v-else>Нет тиражей</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="detailsDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить типографию "{{ itemToDelete?.name }}"?
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
import { ref, onMounted, reactive } from 'vue'
import api from '@/services/api'
import type { PrintingHouse, PrintingHouseFullDetail, PrintingHouseForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false },
  { title: 'Название', key: 'name', sortable: false },
  { title: 'Адрес', key: 'address', sortable: false },
  { title: 'Статус', key: 'is_active', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false },
]

const printingHouses = ref<PrintingHouse[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const detailsDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<PrintingHouse | null>(null)
const selectedItem = ref<PrintingHouse | null>(null)
const fullDetails = ref<PrintingHouseFullDetail | null>(null)
const itemToDelete = ref<PrintingHouse | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<PrintingHouseForm>({
  name: '',
  address: '',
  is_active: true,
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'Обязательное поле') as ValidationRule,
}

async function loadPrintingHouses(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getPrintingHouses(params)
    printingHouses.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Ошибка загрузки типографий')
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: PrintingHouse) {
  editingItem.value = item
  form.name = item.name
  form.address = item.address
  form.is_active = item.is_active
  dialog.value = true
}

function resetForm() {
  form.name = ''
  form.address = ''
  form.is_active = true
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
    if (editingItem.value) {
      await api.updatePrintingHouse(editingItem.value.id, form)
    } else {
      await api.createPrintingHouse(form)
    }
    closeDialog()
    loadPrintingHouses()
  } catch {
    console.error('Ошибка сохранения')
  } finally {
    saving.value = false
  }
}

async function viewDetails(item: PrintingHouse) {
  selectedItem.value = item
  try {
    fullDetails.value = await api.getPrintingHouseFullDetail(item.id)
  } catch {
    console.error('Ошибка загрузки деталей')
  }
  detailsDialog.value = true
}

function confirmDelete(item: PrintingHouse) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deletePrintingHouse(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadPrintingHouses()
  } catch {
    console.error('Ошибка удаления')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadPrintingHouses({ page: 1, itemsPerPage: 20 })
})
</script>

