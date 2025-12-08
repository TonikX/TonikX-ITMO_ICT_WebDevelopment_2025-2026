<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Почтовые отделения</span>
            <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
              Создать почтовое отделение
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="postOffices"
              :loading="loading"
              :items-per-page="20"
              :server-items-length="totalCount"
              @update:options="loadPostOffices"
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

    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ editingItem ? 'Редактировать почтовое отделение' : 'Создать почтовое отделение' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="form.number"
              label="Номер"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-2"
            />
            <v-text-field
              v-model="form.address"
              label="Адрес"
              :rules="[rules.required]"
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

    <v-dialog v-model="detailsDialog" max-width="800px">
      <v-card v-if="selectedItem">
        <v-card-title>Детали почтового отделения</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <p><strong>Номер:</strong> {{ selectedItem.number }}</p>
              <p><strong>Адрес:</strong> {{ selectedItem.address }}</p>
            </v-col>
          </v-row>
          <v-divider class="my-4" />
          <div v-if="fullDetails">
            <h3 class="mb-2">Распределения</h3>
            <v-list v-if="fullDetails.distributions?.length">
              <v-list-item
                v-for="dist in fullDetails.distributions"
                :key="dist.id"
              >
                {{ dist.newspaper.title }} - количество: {{ dist.quantity }}
              </v-list-item>
            </v-list>
            <p v-else>Нет распределений</p>
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
          Вы уверены, что хотите удалить почтовое отделение "{{ itemToDelete?.number }}"?
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
import type { PostOffice, PostOfficeFullDetail, PostOfficeForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false },
  { title: 'Номер', key: 'number', sortable: false },
  { title: 'Адрес', key: 'address', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false },
]

const postOffices = ref<PostOffice[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const detailsDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<PostOffice | null>(null)
const selectedItem = ref<PostOffice | null>(null)
const fullDetails = ref<PostOfficeFullDetail | null>(null)
const itemToDelete = ref<PostOffice | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<PostOfficeForm>({
  number: '',
  address: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'Обязательное поле') as ValidationRule,
}

async function loadPostOffices(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getPostOffices(params)
    postOffices.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Ошибка загрузки почтовых отделений')
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: PostOffice) {
  editingItem.value = item
  form.number = item.number
  form.address = item.address
  dialog.value = true
}

function resetForm() {
  form.number = ''
  form.address = ''
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
      await api.updatePostOffice(editingItem.value.id, form)
    } else {
      await api.createPostOffice(form)
    }
    closeDialog()
    loadPostOffices()
  } catch {
    console.error('Ошибка сохранения')
  } finally {
    saving.value = false
  }
}

async function viewDetails(item: PostOffice) {
  selectedItem.value = item
  try {
    fullDetails.value = await api.getPostOfficeFullDetail(item.id)
  } catch {
    console.error('Ошибка загрузки деталей')
  }
  detailsDialog.value = true
}

function confirmDelete(item: PostOffice) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deletePostOffice(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadPostOffices()
  } catch {
    console.error('Ошибка удаления')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadPostOffices({ page: 1, itemsPerPage: 20 })
})
</script>

