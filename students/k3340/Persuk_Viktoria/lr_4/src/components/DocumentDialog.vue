<template>
  <v-dialog :model-value="modelValue" max-width="600" persistent @update:model-value="$emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>
        {{ editingDocument ? 'Редактировать документ' : 'Добавить документ' }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="formValid">
          <v-select
            v-model="formData.document_type"
            :items="documentTypeOptions"
            label="Тип документа"
            :rules="[v => !!v || 'Обязательное поле']"
            variant="outlined"
            class="mb-4"
          ></v-select>
          <v-text-field
            v-model="formData.url"
            label="URL документа"
            :rules="[v => !!v || 'Обязательное поле', v => /^https?:\/\/.+/.test(v) || 'Должен быть валидный URL']"
            variant="outlined"
            hint="Введите полный URL документа (например, https://example.com/document.pdf)"
            persistent-hint
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="$emit('update:modelValue', false)">Отмена</v-btn>
        <v-btn
          color="primary"
          :loading="saving"
          :disabled="!formValid || saving"
          @click="save"
        >
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, inject } from 'vue'
import * as documentsAPI from '@/api/documents'

const props = defineProps({
  modelValue: Boolean,
  droneId: Number,
  document: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const showSnackbar = inject('showSnackbar')
const saving = ref(false)
const formRef = ref(null)
const formValid = ref(false)
const editingDocument = ref(null)

const formData = ref({
  document_type: '',
  url: '',
})

const documentTypeOptions = [
  { title: 'Сертификат соответствия', value: 'certificate' },
  { title: 'Страховой полис', value: 'insurance' },
  { title: 'Фото дрона', value: 'photo' },
  { title: 'Лицензия/разрешение', value: 'license' },
  { title: 'Прочее', value: 'other' },
]

watch(() => props.document, (newDocument) => {
  if (newDocument) {
    editingDocument.value = newDocument
    formData.value = {
      document_type: newDocument.document_type || '',
      url: newDocument.url || '',
    }
  } else {
    editingDocument.value = null
    resetForm()
  }
}, { immediate: true })

const resetForm = () => {
  formData.value = {
    document_type: '',
    url: '',
  }
}

const save = async () => {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = { ...formData.value }

    if (editingDocument.value) {
      await documentsAPI.updateDocument(editingDocument.value.id, data)
      showSnackbar('Документ успешно обновлён', 'success')
    } else {
      await documentsAPI.createDocument(data, props.droneId)
      showSnackbar('Документ успешно создан', 'success')
    }
    emit('update:modelValue', false)
    emit('saved')
  } catch (error) {
    const message = error.response?.data?.detail ||
                   Object.values(error.response?.data || {})[0]?.[0] ||
                   'Ошибка сохранения документа'
    showSnackbar(message, 'error')
  } finally {
    saving.value = false
  }
}
</script>
