<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      <v-text-field
        v-model="search"
        density="compact"
        variant="outlined"
        hide-details
        label="Поиск"
        style="max-width: 320px"
      />
      <v-btn
        v-if="canWrite"
        class="ml-3"
        color="primary"
        prepend-icon="mdi-plus"
        @click="openCreate"
      >
        Добавить
      </v-btn>
    </v-card-title>

    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-data-table
        :headers="headersValue"
        :items="itemsValue"
        :loading="loading"
        :search="search"
        item-value="id"
      >
        <template v-if="canWrite" #item.actions="{ item }">
          <v-btn size="small" variant="text" icon="mdi-pencil" @click="openEdit(item)" />
          <v-btn size="small" variant="text" icon="mdi-delete" @click="openDelete(item)" />
        </template>

        <template #no-data>
          <div class="pa-6 text-medium-emphasis">Нет данных</div>
        </template>
      </v-data-table>
    </v-card-text>

    <!-- create/edit dialog -->
    <v-dialog v-model="dialog" max-width="760">
      <v-card>
        <v-card-title class="text-h6">{{ dialogTitle }}</v-card-title>

        <v-card-text>
          <v-form ref="formRef" @submit.prevent="onSaveClick">
            <div class="d-flex flex-wrap" style="gap: 12px">
              <template v-for="field in fieldsValue" :key="field.key">
                <div :style="{ flex: field.fullWidth ? '1 0 100%' : '1 0 320px' }">
                  <component
                    :is="resolveComponent(field)"
                    v-model="model[field.key]"
                    :label="field.label"
                    :items="field.items"
                    :item-title="field.itemTitle"
                    :item-value="field.itemValue"
                    :type="field.type"
                    :clearable="true"
                    variant="outlined"
                    density="compact"
                    :rules="normalizeRules(field.rules)"
                    :disabled="!!field.disabled"
                  />
                </div>
              </template>

              <div v-if="fieldsValue.length === 0" class="text-medium-emphasis">
                Поля формы не заданы (fields пустой).
              </div>
            </div>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :disabled="!canWrite" @click="onSaveClick">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- confirm delete -->
    <v-dialog v-model="confirmDelete" max-width="520">
      <v-card>
        <v-card-title class="text-h6">Удалить запись?</v-card-title>
        <v-card-text>
          <div>Это действие нельзя отменить.</div>
          <div class="mt-2 text-medium-emphasis">ID: {{ selected?.id }}</div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="confirmDelete=false">Отмена</v-btn>
          <v-btn color="error" :disabled="!canWrite" @click="doDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { VTextField, VSelect, VTextarea, VCheckbox } from 'vuetify/components'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  title: { type: String, required: false, default: '' },
  headers: { type: [Array, Object], required: true },
  fields: { type: [Array, Object], required: true },
  items: { type: [Array, Object], required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
  canWrite: { type: Boolean, default: undefined },
})

const emits = defineEmits(['create', 'update', 'delete'])

const search = ref('')
const dialog = ref(false)
const confirmDelete = ref(false)

const selected = ref(null)
const model = ref({})
const mode = ref('create')
const formRef = ref(null)

const auth = useAuthStore()
auth.hydrate()

const canWrite = computed(() => {
  if (props.canWrite !== undefined) return props.canWrite
  const u = auth.user
  return !!(u && (u.is_staff || u.is_superuser))
})

const dialogTitle = computed(() => (mode.value === 'create' ? 'Создание' : 'Редактирование'))

const headersValue = computed(() => {
  const h = Array.isArray(props.headers) ? props.headers : (props.headers?.value || [])
  return canWrite.value ? h : h.filter((x) => x.key !== 'actions')
})

const itemsValue = computed(() => {
  if (Array.isArray(props.items)) return props.items
  if (props.items && Array.isArray(props.items.value)) return props.items.value
  return []
})

const fieldsValue = computed(() => {
  if (Array.isArray(props.fields)) return props.fields
  if (props.fields && Array.isArray(props.fields.value)) return props.fields.value
  return []
})

function unwrapItem(item) {
  return item?.raw ?? item
}

function normalizeRules(rules) {
  if (!Array.isArray(rules)) return []
  return rules.map((r) => {
    if (typeof r === 'function') return r
    if (typeof r === 'string') {
      try {
        const fn = new Function(`return (${r})`)()
        return typeof fn === 'function' ? fn : () => true
      } catch {
        return () => true
      }
    }
    return () => true
  })
}

function resolveComponent(field) {
  // если передали объект-компонент (редко) — используем его
  if (field?.component && typeof field.component === 'object') return field.component

  const c = field?.component
  if (c === 'v-select' || c === 'VSelect' || field?.type === 'select') return VSelect
  if (c === 'v-textarea' || c === 'VTextarea' || field?.type === 'textarea') return VTextarea
  if (c === 'v-checkbox' || c === 'VCheckbox' || field?.type === 'checkbox') return VCheckbox
  return VTextField
}

function resetState() {
  model.value = {}
  selected.value = null
  mode.value = 'create'
}

function openCreate() {
  if (!canWrite.value) return
  resetState()
  dialog.value = true
}

function openEdit(item) {
  if (!canWrite.value) return
  const row = unwrapItem(item)
  mode.value = 'edit'
  selected.value = row
  model.value = { ...row }
  dialog.value = true
}

function openDelete(item) {
  if (!canWrite.value) return
  selected.value = unwrapItem(item)
  confirmDelete.value = true
}

function closeDialog() {
  dialog.value = false
}

async function onSaveClick() {
  if (!canWrite.value) return

  const form = formRef.value
  if (form?.validate) {
    const res = await form.validate()
    if (!res.valid) return
  }

  if (mode.value === 'create') {
    emits('create', model.value)
  } else {
    if (!selected.value?.id) return
    emits('update', { id: selected.value.id, payload: model.value })
  }

  dialog.value = false
}

function doDelete() {
  if (!canWrite.value) return
  if (!selected.value?.id) return
  emits('delete', selected.value.id)
  confirmDelete.value = false
}

watch(dialog, (v) => {
  if (!v) resetState()
})
</script>
