<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Учителя</span>
            <v-btn color="primary" @click="openDialog(null)">
              <v-icon left>mdi-plus</v-icon>
              Добавить учителя
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="teachers"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.full_name="{ item }">
                {{ `${item.last_name} ${item.first_name} ${item.middle_name || ''}`.trim() }}
              </template>
              <template v-slot:item.classroom="{ item }">
                <span v-if="item.classroom_id">
                  {{ referenceStore.getClassroomLabel(item.classroom_id) }}
                </span>
                <span v-else>-</span>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="openDialog(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteTeacher(item.id)">
                  mdi-delete
                </v-icon>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          {{ editingTeacher ? 'Редактировать учителя' : 'Добавить учителя' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="form.first_name"
              label="Имя"
              variant="outlined"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.last_name"
              label="Фамилия"
              variant="outlined"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.middle_name"
              label="Отчество"
              variant="outlined"
            ></v-text-field>
            <v-select
              v-model.number="form.classroom_id"
              label="Кабинет (необязательно)"
              :items="classroomItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              clearable
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveTeacher">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import api from '@/api/client'
import { useReferenceStore } from '@/stores/reference'

const referenceStore = useReferenceStore()
const teachers = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingTeacher = ref(null)
const form = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  classroom_id: null
})

const classroomItems = computed(() => {
  const items = [{ text: 'Не выбран', value: null }]
  if (referenceStore.classrooms && referenceStore.classrooms.length > 0) {
    referenceStore.classrooms.forEach(c => {
      items.push({
        text: `Кабинет ${c.room_number}`,
        value: c.id
      })
    })
  }
  return items
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Кабинет', key: 'classroom' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const loadTeachers = async () => {
  loading.value = true
  try {
    const response = await api.get('/teachers')
    teachers.value = response.data || []
  } catch (error) {
    console.error('Ошибка загрузки учителей:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = async (teacher) => {
  // Убеждаемся, что кабинеты загружены перед открытием диалога
  if (!referenceStore.classrooms || referenceStore.classrooms.length === 0) {
    await referenceStore.loadClassrooms()
  }
  
  if (teacher) {
    // Находим актуальный объект из списка, чтобы избежать проблем с устаревшими ссылками
    const currentTeacher = teachers.value.find(t => t.id === teacher.id) || teacher
    editingTeacher.value = { ...currentTeacher } // Создаем копию объекта
  } else {
    editingTeacher.value = null
  }
  
  // Открываем диалог
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  // Сбрасываем редактируемого учителя после закрытия диалога
  setTimeout(() => {
    editingTeacher.value = null
    form.value = {
      first_name: '',
      last_name: '',
      middle_name: null,
      classroom_id: null
    }
  }, 300) // Небольшая задержка для анимации закрытия
}

const saveTeacher = async () => {
  try {
    if (editingTeacher.value) {
      await api.put(`/teachers/${editingTeacher.value.id}`, form.value)
    } else {
      await api.post('/teachers', form.value)
    }
    await loadTeachers() // Обновляем список
    closeDialog()
  } catch (error) {
    console.error('Ошибка сохранения учителя:', error)
    alert(error.response?.data?.error || 'Ошибка сохранения')
  }
}

const deleteTeacher = async (id) => {
  if (confirm('Вы уверены, что хотите удалить этого учителя?')) {
    try {
      await api.delete(`/teachers/${id}`)
      loadTeachers()
    } catch (error) {
      console.error('Ошибка удаления учителя:', error)
      alert(error.response?.data?.error || 'Ошибка удаления')
    }
  }
}

// Отслеживаем открытие/закрытие диалога для заполнения/сброса формы
watch(dialog, async (isOpen) => {
  if (isOpen) {
    // Когда диалог открывается, заполняем форму
    await nextTick()
    if (editingTeacher.value) {
      form.value = {
        first_name: editingTeacher.value.first_name || '',
        last_name: editingTeacher.value.last_name || '',
        middle_name: editingTeacher.value.middle_name || null,
        classroom_id: editingTeacher.value.classroom_id ? Number(editingTeacher.value.classroom_id) : null
      }
    } else {
      // Если редактируемого учителя нет, сбрасываем форму
      form.value = {
        first_name: '',
        last_name: '',
        middle_name: null,
        classroom_id: null
      }
    }
  } else {
    // При закрытии диалога сбрасываем редактируемого учителя через небольшую задержку
    setTimeout(() => {
      editingTeacher.value = null
    }, 300)
  }
})

onMounted(async () => {
  await referenceStore.loadClassrooms()
  await loadTeachers()
})
</script>

