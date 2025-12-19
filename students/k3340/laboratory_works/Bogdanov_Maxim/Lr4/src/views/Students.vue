<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Ученики</span>
            <v-btn color="primary" @click="openDialog(null)">
              <v-icon left>mdi-plus</v-icon>
              Добавить ученика
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Выбор класса -->
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-select
                  v-model="selectedClassId"
                  label="Выберите класс"
                  :items="classItems"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  clearable
                  @update:model-value="onClassChange"
                ></v-select>
              </v-col>
            </v-row>
            
            <v-data-table
              :headers="headers"
              :items="filteredStudents"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.full_name="{ item }">
                {{ `${item.last_name} ${item.first_name} ${item.middle_name || ''}`.trim() }}
              </template>
              <template v-slot:item.class_name="{ item }">
                <span v-if="item.class_id">{{ referenceStore.getClassLabel(item.class_id) }}</span>
                <span v-else>-</span>
              </template>
              <template v-slot:item.gender="{ item }">
                {{ item.gender_id === 1 ? 'Мужской' : item.gender_id === 2 ? 'Женский' : '-' }}
              </template>
              <template v-slot:item.birth_date="{ item }">
                {{ item.birth_date ? new Date(item.birth_date).toLocaleDateString('ru-RU') : '-' }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="openDialog(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteStudent(item.id)">
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
          {{ editingStudent ? 'Редактировать ученика' : 'Добавить ученика' }}
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
              v-model.number="form.class_id"
              label="Класс"
              :items="classItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model="form.gender"
              label="Пол"
              :items="genders"
              variant="outlined"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveStudent">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/client'
import { useReferenceStore } from '@/stores/reference'

const route = useRoute()
const router = useRouter()
const referenceStore = useReferenceStore()
const students = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingStudent = ref(null)
const selectedClassId = ref(null)
const form = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  class_id: null,
  gender: '',
  birth_date: ''
})

const classItems = computed(() => {
  return referenceStore.classes.map(c => ({
    text: `${c.grade}${c.letter}`,
    value: c.id
  }))
})

const genders = [
  { title: 'Мужской', value: 'male' },
  { title: 'Женский', value: 'female' }
]

const filteredStudents = computed(() => {
  if (!selectedClassId.value) {
    return students.value
  }
  return students.value.filter(s => s.class_id === selectedClassId.value)
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Класс', key: 'class_name' },
  { title: 'Пол', key: 'gender', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false }
]

const onClassChange = () => {
  // Обновляем URL с query параметром
  if (selectedClassId.value) {
    router.push({ query: { classId: selectedClassId.value } })
  } else {
    router.push({ query: {} })
  }
}

const loadStudents = async () => {
  loading.value = true
  try {
    const response = await api.get('/students')
    students.value = response.data || []
  } catch (error) {
    console.error('Ошибка загрузки учеников:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = async (student) => {
  // Убеждаемся, что классы загружены перед открытием диалога
  if (!referenceStore.classes || referenceStore.classes.length === 0) {
    await referenceStore.loadClasses()
  }
  
  if (student) {
    // Находим актуальный объект из списка, чтобы избежать проблем с устаревшими ссылками
    const currentStudent = students.value.find(s => s.id === student.id) || student
    editingStudent.value = { ...currentStudent } // Создаем копию объекта
  } else {
    editingStudent.value = null
  }
  
  // Открываем диалог
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  // Сбрасываем редактируемого ученика после закрытия диалога
  setTimeout(() => {
    editingStudent.value = null
    form.value = {
      first_name: '',
      last_name: '',
      middle_name: null,
      class_id: null,
      gender: '',
      birth_date: ''
    }
  }, 300) // Небольшая задержка для анимации закрытия
}

const saveStudent = async () => {
  try {
    // Преобразуем gender в gender_id: 'male' -> 1, 'female' -> 2
    const genderId = form.value.gender === 'male' ? 1 : form.value.gender === 'female' ? 2 : null
    
    if (!genderId) {
      alert('Необходимо выбрать пол')
      return
    }
    
    // Формируем данные для отправки (без birth_date, так как бэкенд его не поддерживает)
    const requestData = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      middle_name: form.value.middle_name || null,
      class_id: form.value.class_id,
      gender_id: genderId
    }
    
    if (editingStudent.value) {
      await api.put(`/students/${editingStudent.value.id}`, requestData)
    } else {
      await api.post('/students', requestData)
    }
    await loadStudents() // Обновляем список
    closeDialog()
  } catch (error) {
    console.error('Ошибка сохранения ученика:', error)
    alert(error.response?.data?.error || 'Ошибка сохранения')
  }
}

const deleteStudent = async (id) => {
  if (confirm('Вы уверены, что хотите удалить этого ученика?')) {
    try {
      await api.delete(`/students/${id}`)
      loadStudents()
    } catch (error) {
      console.error('Ошибка удаления ученика:', error)
      alert(error.response?.data?.error || 'Ошибка удаления')
    }
  }
}

onMounted(async () => {
  await referenceStore.loadClasses()
  await loadStudents()
  
  // Проверяем query параметр из URL
  if (route.query.classId) {
    const classId = parseInt(route.query.classId)
    if (!isNaN(classId)) {
      selectedClassId.value = classId
    }
  }
})

// Следим за изменениями query параметра
watch(() => route.query.classId, (newClassId) => {
  if (newClassId) {
    const classId = parseInt(newClassId)
    if (!isNaN(classId) && classId !== selectedClassId.value) {
      selectedClassId.value = classId
    }
  } else {
    selectedClassId.value = null
  }
})

// Отслеживаем открытие/закрытие диалога для заполнения/сброса формы
watch(dialog, async (isOpen) => {
  if (isOpen) {
    // Когда диалог открывается, заполняем форму
    await nextTick()
    if (editingStudent.value) {
      // Преобразуем gender_id в gender: 1 -> 'male', 2 -> 'female'
      const gender = editingStudent.value.gender_id === 1 ? 'male' : editingStudent.value.gender_id === 2 ? 'female' : ''
      
      form.value = {
        first_name: editingStudent.value.first_name || '',
        last_name: editingStudent.value.last_name || '',
        middle_name: editingStudent.value.middle_name || null,
        class_id: editingStudent.value.class_id ? Number(editingStudent.value.class_id) : null,
        gender: gender,
        birth_date: '' // birth_date не поддерживается бэкендом
      }
    } else {
      // Если редактируемого ученика нет, сбрасываем форму
      form.value = {
        first_name: '',
        last_name: '',
        middle_name: null,
        class_id: null,
        gender: '',
        birth_date: ''
      }
    }
  } else {
    // При закрытии диалога сбрасываем редактируемого ученика через небольшую задержку
    setTimeout(() => {
      editingStudent.value = null
    }, 300)
  }
})
</script>

