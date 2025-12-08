<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Газеты</span>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
              Создать газету
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="newspapers"
              :loading="loading"
              :items-per-page="20"
              :server-items-length="totalCount"
              @update:options="loadNewspapers"
            >
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

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ editingItem ? 'Редактировать газету' : 'Создать газету' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.title"
              label="Название"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.publication_index"
              label="Индекс издания"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.editor_first_name"
              label="Имя редактора"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.editor_last_name"
              label="Фамилия редактора"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.editor_middle_name"
              label="Отчество редактора"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.price_per_copy"
              label="Цена за экземпляр"
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

    <!-- Диалог деталей -->
    <v-dialog v-model="detailsDialog" max-width="800px">
      <v-card v-if="selectedItem">
        <v-card-title>Детали газеты</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <p><strong>Название:</strong> {{ selectedItem.title }}</p>
              <p><strong>Индекс:</strong> {{ selectedItem.publication_index }}</p>
              <p><strong>Цена:</strong> {{ selectedItem.price_per_copy }} ₽</p>
            </v-col>
            <v-col cols="12" md="6">
              <p><strong>Редактор:</strong> {{ selectedItem.editor_full_name }}</p>
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
                Тираж: {{ run.circulation }}
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

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить газету "{{ itemToDelete?.title }}"?
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
import type { Newspaper, NewspaperFullDetail, NewspaperForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false },
  { title: 'Название', key: 'title', sortable: false },
  { title: 'Индекс', key: 'publication_index', sortable: false },
  { title: 'Редактор', key: 'editor_full_name', sortable: false },
  { title: 'Цена', key: 'price_per_copy', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false },
]

const newspapers = ref<Newspaper[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const detailsDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<Newspaper | null>(null)
const selectedItem = ref<Newspaper | null>(null)
const fullDetails = ref<NewspaperFullDetail | null>(null)
const itemToDelete = ref<Newspaper | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<NewspaperForm>({
  title: '',
  publication_index: '',
  editor_first_name: '',
  editor_last_name: '',
  editor_middle_name: '',
  price_per_copy: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'Обязательное поле') as ValidationRule,
  positive: ((v: string | number | null | undefined) => {
    const num = typeof v === 'string' ? parseFloat(v) : v
    return (num && num > 0) || 'Значение должно быть положительным'
  }) as ValidationRule,
}

async function loadNewspapers(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getNewspapers(params)
    newspapers.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Ошибка загрузки газет')
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: Newspaper) {
  editingItem.value = item
  form.title = item.title
  form.publication_index = item.publication_index
  form.editor_first_name = item.editor_first_name
  form.editor_last_name = item.editor_last_name
  form.editor_middle_name = item.editor_middle_name || ''
  form.price_per_copy = item.price_per_copy
  dialog.value = true
}

function resetForm() {
  form.title = ''
  form.publication_index = ''
  form.editor_first_name = ''
  form.editor_last_name = ''
  form.editor_middle_name = ''
  form.price_per_copy = ''
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
      await api.updateNewspaper(editingItem.value.id, form)
    } else {
      await api.createNewspaper(form)
    }
    closeDialog()
    loadNewspapers()
  } catch {
    console.error('Ошибка сохранения')
  } finally {
    saving.value = false
  }
}

async function viewDetails(item: Newspaper) {
  selectedItem.value = item
  try {
    fullDetails.value = await api.getNewspaperFullDetail(item.id)
  } catch {
    console.error('Ошибка загрузки деталей')
  }
  detailsDialog.value = true
}

function confirmDelete(item: Newspaper) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deleteNewspaper(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadNewspapers()
  } catch {
    console.error('Ошибка удаления')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadNewspapers({ page: 1, itemsPerPage: 20 })
})
</script>

