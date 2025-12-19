<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Оценки</span>
            <v-btn 
              v-if="canEdit" 
              color="primary" 
              @click="openDialog(null)"
            >
              <v-icon left>mdi-plus</v-icon>
              Добавить оценку
            </v-btn>
          </v-card-title>
          <v-card-text>
            <!-- Фильтры -->
            <v-row class="mb-4">
              <v-col cols="12" md="3">
                <v-select
                  v-model="filters.classId"
                  label="Класс"
                  :items="classItems"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  clearable
                  @update:model-value="applyFilters"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="filters.studentId"
                  label="Ученик"
                  :items="filteredStudentItems"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  clearable
                  @update:model-value="applyFilters"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model.number="filters.subjectId"
                  label="Предмет"
                  :items="subjectItems"
                  item-title="text"
                  item-value="value"
                  variant="outlined"
                  clearable
                  @update:model-value="applyFilters"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3" class="d-flex align-center">
                <v-btn 
                  color="secondary" 
                  @click="clearFilters"
                  block
                >
                  Сбросить фильтры
                </v-btn>
              </v-col>
            </v-row>

            <v-data-table
              :headers="headers"
              :items="filteredGrades"
              :loading="loading"
              item-key="id"
            >
              <template v-slot:item.student_name="{ item }">
                {{ referenceStore.getStudentLabel(item.student_id) }}
              </template>
              <template v-slot:item.class_name="{ item }">
                {{ getStudentClass(item.student_id) }}
              </template>
              <template v-slot:item.subject_name="{ item }">
                <span v-if="item.subject_id">{{ referenceStore.getSubjectLabel(item.subject_id) }}</span>
                <span v-else>-</span>
              </template>
              <template v-slot:item.period_name="{ item }">
                <span v-if="item.grading_period_id">{{ referenceStore.getGradingPeriodLabel(item.grading_period_id) }}</span>
                <span v-else>-</span>
              </template>
              <template v-slot:item.grade="{ item }">
                <v-chip :color="getGradeColor(item.grade)" dark>
                  {{ item.grade }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon 
                  v-if="canEdit" 
                  small 
                  class="mr-2" 
                  @click="openDialog(item)"
                >
                  mdi-pencil
                </v-icon>
                <v-icon 
                  v-if="canEdit" 
                  small 
                  @click="deleteGrade(item.id)"
                >
                  mdi-delete
                </v-icon>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingGrade ? 'Редактировать оценку' : 'Добавить оценку' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-select
              v-model.number="form.class_id"
              label="Класс"
              :items="classItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
              @update:model-value="onClassChange"
            ></v-select>
            <v-select
              v-model.number="form.student_id"
              label="Ученик"
              :items="formStudentItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model.number="form.subject_id"
              label="Предмет"
              :items="subjectItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model.number="form.grading_period_id"
              label="Период оценивания"
              :items="gradingPeriodItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model.number="form.grade"
              label="Оценка"
              :items="gradeOptions"
              variant="outlined"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveGrade">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useReferenceStore } from '@/stores/reference'
import api from '@/api/client'

const authStore = useAuthStore()
const referenceStore = useReferenceStore()
const grades = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingGrade = ref(null)
const form = ref({
  class_id: null,
  student_id: null,
  subject_id: null,
  grading_period_id: null,
  grade: null
})

const filters = ref({
  classId: null,
  studentId: null,
  subjectId: null
})

const gradeOptions = [
  { title: '5 (Отлично)', value: 5 },
  { title: '4 (Хорошо)', value: 4 },
  { title: '3 (Удовлетворительно)', value: 3 },
  { title: '2 (Неудовлетворительно)', value: 2 }
]

const canEdit = computed(() => {
  const role = authStore.user?.role
  return role === 'admin' || role === 'teacher'
})

const classItems = computed(() => {
  return referenceStore.classes.map(c => ({
    text: `${c.grade}${c.letter}`,
    value: c.id
  }))
})

const subjectItems = computed(() => {
  return referenceStore.subjects.map(s => ({
    text: s.name,
    value: s.id
  }))
})

const gradingPeriodItems = computed(() => {
  return referenceStore.gradingPeriods.map(p => ({
    text: p.name,
    value: p.id
  }))
})

const allStudentItems = computed(() => {
  return referenceStore.students.map(s => ({
    text: `${s.last_name} ${s.first_name} ${s.middle_name || ''}`.trim(),
    value: s.id,
    classId: s.class_id
  }))
})

const filteredStudentItems = computed(() => {
  if (!filters.value.classId) {
    return allStudentItems.value
  }
  return allStudentItems.value.filter(s => s.classId === filters.value.classId)
})

const formStudentItems = computed(() => {
  if (!form.value.class_id) {
    return []
  }
  return allStudentItems.value.filter(s => s.classId === form.value.class_id)
})

const filteredGrades = computed(() => {
  let result = grades.value

  if (filters.value.classId) {
    const classStudentIds = referenceStore.students
      .filter(s => s.class_id === filters.value.classId)
      .map(s => s.id)
    result = result.filter(g => classStudentIds.includes(g.student_id))
  }

  if (filters.value.studentId) {
    result = result.filter(g => g.student_id === filters.value.studentId)
  }

  if (filters.value.subjectId) {
    result = result.filter(g => g.subject_id === filters.value.subjectId)
  }

  return result
})

const headers = [
  { title: 'Ученик', key: 'student_name' },
  { title: 'Класс', key: 'class_name' },
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Период', key: 'period_name' },
  { title: 'Оценка', key: 'grade' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const getStudentClass = (studentId) => {
  const student = referenceStore.students.find(s => s.id === studentId)
  if (!student) return '-'
  return referenceStore.getClassLabel(student.class_id)
}

const getGradeColor = (grade) => {
  if (grade === 5) return 'success'
  if (grade === 4) return 'info'
  if (grade === 3) return 'warning'
  return 'error'
}

const loadGrades = async () => {
  loading.value = true
  try {
    const response = await api.get('/grades')
    grades.value = response.data || []
  } catch (error) {
    console.error('Ошибка загрузки оценок:', error)
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  // Фильтрация происходит через computed свойство
}

const clearFilters = () => {
  filters.value = {
    classId: null,
    studentId: null,
    subjectId: null
  }
}

const onClassChange = () => {
  form.value.student_id = null
}

const openDialog = async (grade) => {
  // Убеждаемся, что все справочные данные загружены
  if (!referenceStore.classes || referenceStore.classes.length === 0 || 
      !referenceStore.students || referenceStore.students.length === 0 || 
      !referenceStore.subjects || referenceStore.subjects.length === 0 || 
      !referenceStore.gradingPeriods || referenceStore.gradingPeriods.length === 0) {
    await referenceStore.loadAll()
  }
  
  if (grade) {
    // Находим актуальный объект из списка, чтобы избежать проблем с устаревшими ссылками
    const currentGrade = grades.value.find(g => g.id === grade.id) || grade
    editingGrade.value = { ...currentGrade } // Создаем копию объекта
  } else {
    editingGrade.value = null
  }
  
  // Открываем диалог
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  // Сбрасываем редактируемую оценку после закрытия диалога
  setTimeout(() => {
    editingGrade.value = null
    form.value = {
      class_id: null,
      student_id: null,
      subject_id: null,
      grading_period_id: null,
      grade: null
    }
  }, 300) // Небольшая задержка для анимации закрытия
}

const saveGrade = async () => {
  try {
    const payload = {
      student_id: form.value.student_id,
      subject_id: form.value.subject_id,
      grading_period_id: form.value.grading_period_id,
      grade: form.value.grade
    }
    
    if (editingGrade.value) {
      await api.put(`/grades/${editingGrade.value.id}`, payload)
    } else {
      await api.post('/grades', payload)
    }
    await loadGrades() // Обновляем список
    closeDialog()
  } catch (error) {
    console.error('Ошибка сохранения оценки:', error)
    alert(error.response?.data?.error || 'Ошибка сохранения')
  }
}

const deleteGrade = async (id) => {
  if (confirm('Вы уверены, что хотите удалить эту оценку?')) {
    try {
      await api.delete(`/grades/${id}`)
      loadGrades()
    } catch (error) {
      console.error('Ошибка удаления оценки:', error)
      alert(error.response?.data?.error || 'Ошибка удаления')
    }
  }
}

// Отслеживаем открытие/закрытие диалога для заполнения/сброса формы
watch(dialog, async (isOpen) => {
  if (isOpen) {
    // Когда диалог открывается, заполняем форму
    await nextTick()
    if (editingGrade.value) {
      const student = referenceStore.students.find(s => s.id === editingGrade.value.student_id)
      form.value = {
        class_id: student?.class_id ? Number(student.class_id) : null,
        student_id: editingGrade.value.student_id ? Number(editingGrade.value.student_id) : null,
        subject_id: editingGrade.value.subject_id ? Number(editingGrade.value.subject_id) : null,
        grading_period_id: editingGrade.value.grading_period_id ? Number(editingGrade.value.grading_period_id) : null,
        grade: editingGrade.value.grade ? Number(editingGrade.value.grade) : null
      }
    } else {
      // Если редактируемой оценки нет, сбрасываем форму
      form.value = {
        class_id: null,
        student_id: null,
        subject_id: null,
        grading_period_id: null,
        grade: null
      }
    }
  } else {
    // При закрытии диалога сбрасываем редактируемую оценку через небольшую задержку
    setTimeout(() => {
      editingGrade.value = null
    }, 300)
  }
})

onMounted(async () => {
  await referenceStore.loadAll()
  await loadGrades()
})
</script>
