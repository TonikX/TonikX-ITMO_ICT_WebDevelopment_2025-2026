<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Классы</span>
            <v-btn color="primary" @click="openDialog(null)">
              <v-icon left>mdi-plus</v-icon>
              Добавить класс
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="classes"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.class_name="{ item }">
                <v-btn
                  variant="text"
                  color="primary"
                  @click="viewClassStudents(item.id)"
                >
                  {{ `${item.grade}${item.letter}` }}
                </v-btn>
              </template>
              <template v-slot:item.academic_year="{ item }">
                <span v-if="item.academic_year_id">
                  {{ referenceStore.academicYears.find(ay => ay.id === item.academic_year_id)?.name || '-' }}
                </span>
                <span v-else>-</span>
              </template>
              <template v-slot:item.class_teacher="{ item }">
                {{ item.class_teacher_id ? referenceStore.getTeacherLabel(item.class_teacher_id) : '-' }}
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="openDialog(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteClass(item.id)">
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
          {{ editingClass ? 'Редактировать класс' : 'Добавить класс' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model.number="form.grade"
              label="Класс (номер)"
              type="number"
              variant="outlined"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.letter"
              label="Буква класса"
              variant="outlined"
              required
            ></v-text-field>
            <v-select
              v-model.number="form.academic_year_id"
              label="Учебный год"
              :items="academicYearItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model.number="form.class_teacher_id"
              label="Классный руководитель (необязательно)"
              :items="teacherItems"
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
          <v-btn color="primary" @click="saveClass">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/client'
import { useReferenceStore } from '@/stores/reference'

const router = useRouter()

const referenceStore = useReferenceStore()
const classes = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingClass = ref(null)
const form = ref({
  grade: null,
  letter: '',
  academic_year_id: null,
  class_teacher_id: null
})

const teacherItems = computed(() => {
  return referenceStore.teachers.map(t => ({
    text: `${t.last_name} ${t.first_name} ${t.middle_name || ''}`.trim(),
    value: t.id
  }))
})

const academicYearItems = computed(() => {
  return referenceStore.academicYears.map(ay => ({
    text: ay.name,
    value: ay.id
  }))
})

const headers = [
  { title: 'Класс', key: 'class_name' },
  { title: 'Учебный год', key: 'academic_year' },
  { title: 'Классный руководитель', key: 'class_teacher' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const loadClasses = async () => {
  loading.value = true
  try {
    const response = await api.get('/classes')
    classes.value = response.data || []
  } catch (error) {
    console.error('Ошибка загрузки классов:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = async (classItem) => {
  // Убеждаемся, что справочные данные загружены
  if (!referenceStore.academicYears || referenceStore.academicYears.length === 0) {
    await referenceStore.loadAcademicYears()
  }
  if (!referenceStore.teachers || referenceStore.teachers.length === 0) {
    await referenceStore.loadTeachers()
  }
  
  if (classItem) {
    // Находим актуальный объект из списка, чтобы избежать проблем с устаревшими ссылками
    const currentClass = classes.value.find(c => c.id === classItem.id) || classItem
    editingClass.value = { ...currentClass } // Создаем копию объекта
  } else {
    editingClass.value = null
  }
  
  // Открываем диалог
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  // Сбрасываем редактируемый класс после закрытия диалога
  setTimeout(() => {
    editingClass.value = null
    form.value = {
      grade: null,
      letter: '',
      academic_year_id: null,
      class_teacher_id: null
    }
  }, 300) // Небольшая задержка для анимации закрытия
}

const saveClass = async () => {
  try {
    if (editingClass.value) {
      await api.put(`/classes/${editingClass.value.id}`, form.value)
    } else {
      await api.post('/classes', form.value)
    }
    await loadClasses() // Обновляем список
    closeDialog()
  } catch (error) {
    console.error('Ошибка сохранения класса:', error)
    alert(error.response?.data?.error || 'Ошибка сохранения')
  }
}

const deleteClass = async (id) => {
  if (confirm('Вы уверены, что хотите удалить этот класс?')) {
    try {
      await api.delete(`/classes/${id}`)
      loadClasses()
    } catch (error) {
      console.error('Ошибка удаления класса:', error)
      alert(error.response?.data?.error || 'Ошибка удаления')
    }
  }
}

const viewClassStudents = (classId) => {
  router.push({ name: 'students', query: { classId } })
}

// Отслеживаем открытие/закрытие диалога для заполнения/сброса формы
watch(dialog, async (isOpen) => {
  if (isOpen) {
    // Когда диалог открывается, заполняем форму
    await nextTick()
    if (editingClass.value) {
      form.value = {
        grade: editingClass.value.grade ? Number(editingClass.value.grade) : null,
        letter: editingClass.value.letter || '',
        academic_year_id: editingClass.value.academic_year_id ? Number(editingClass.value.academic_year_id) : null,
        class_teacher_id: editingClass.value.class_teacher_id ? Number(editingClass.value.class_teacher_id) : null
      }
    } else {
      // Если редактируемого класса нет, сбрасываем форму
      form.value = {
        grade: null,
        letter: '',
        academic_year_id: null,
        class_teacher_id: null
      }
    }
  } else {
    // При закрытии диалога сбрасываем редактируемый класс через небольшую задержку
    setTimeout(() => {
      editingClass.value = null
    }, 300)
  }
})

onMounted(async () => {
  await referenceStore.loadTeachers()
  await referenceStore.loadAcademicYears()
  await loadClasses()
})
</script>

