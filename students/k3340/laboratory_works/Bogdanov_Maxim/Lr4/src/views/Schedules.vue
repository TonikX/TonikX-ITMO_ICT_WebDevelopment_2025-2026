<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Расписание</span>
            <v-btn color="primary" @click="openDialog(null)">
              <v-icon left>mdi-plus</v-icon>
              Добавить запись
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

            <!-- Расписание по дням недели -->
            <div v-if="selectedClassId && !loading">
              <v-card
                v-for="weekday in weekdays"
                :key="weekday.id"
                class="mb-4"
              >
                <v-card-title>{{ weekday.name }}</v-card-title>
                <v-card-text>
                  <v-table>
                    <thead>
                      <tr>
                        <th>Урок</th>
                        <th>Предмет</th>
                        <th>Учитель</th>
                        <th>Кабинет</th>
                        <th v-if="canEdit">Действия</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="lesson in getLessonsForWeekday(weekday.id)"
                        :key="`${weekday.id}-${lesson.lesson_number}`"
                      >
                        <td>{{ lesson.lesson_number }}</td>
                        <td>{{ referenceStore.getSubjectLabel(lesson.subject_id) }}</td>
                        <td>{{ referenceStore.getTeacherLabel(lesson.teacher_id) }}</td>
                        <td>{{ referenceStore.getClassroomLabel(lesson.classroom_id) }}</td>
                        <td v-if="canEdit">
                          <v-icon small class="mr-2" @click="openDialog(lesson)">
                            mdi-pencil
                          </v-icon>
                          <v-icon small @click="deleteSchedule(lesson.id)">
                            mdi-delete
                          </v-icon>
                        </td>
                      </tr>
                      <tr v-if="getLessonsForWeekday(weekday.id).length === 0">
                        <td :colspan="canEdit ? 5 : 4" class="text-center text-grey">
                          Нет уроков
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-card-text>
              </v-card>
            </div>

            <!-- Сообщение если класс не выбран -->
            <v-alert
              v-else-if="!selectedClassId && !loading"
              type="info"
              variant="tonal"
            >
              Выберите класс для просмотра расписания
            </v-alert>

            <v-progress-linear
              v-if="loading"
              indeterminate
              color="primary"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          {{ editingSchedule ? 'Редактировать расписание' : 'Добавить запись расписания' }}
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
            ></v-select>
            <v-select
              v-model.number="form.weekday_id"
              label="День недели"
              :items="weekdayItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-text-field
              v-model.number="form.lesson_number"
              label="Номер урока"
              type="number"
              variant="outlined"
              required
              min="1"
              max="8"
            ></v-text-field>
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
              v-model.number="form.teacher_id"
              label="Учитель"
              :items="teacherItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
            <v-select
              v-model.number="form.classroom_id"
              label="Кабинет"
              :items="classroomItems"
              item-title="text"
              item-value="value"
              variant="outlined"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveSchedule">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/client'
import { useReferenceStore } from '@/stores/reference'

const authStore = useAuthStore()
const referenceStore = useReferenceStore()
const schedules = ref([])
const loading = ref(false)
const dialog = ref(false)
const editingSchedule = ref(null)
const selectedClassId = ref(null)
const form = ref({
  class_id: null,
  weekday_id: null,
  lesson_number: null,
  subject_id: null,
  teacher_id: null,
  classroom_id: null
})

const canEdit = computed(() => {
  const role = authStore.user?.role
  return role === 'admin'
})

const classItems = computed(() => {
  return referenceStore.classes.map(c => ({
    text: `${c.grade}${c.letter}`,
    value: c.id
  }))
})

const teacherItems = computed(() => {
  return referenceStore.teachers.map(t => ({
    text: `${t.last_name} ${t.first_name} ${t.middle_name || ''}`.trim(),
    value: t.id
  }))
})

const subjectItems = computed(() => {
  return referenceStore.subjects.map(s => ({
    text: s.name,
    value: s.id
  }))
})

const classroomItems = computed(() => {
  return referenceStore.classrooms.map(c => ({
    text: `Кабинет ${c.room_number}`,
    value: c.id
  }))
})

const weekdayItems = computed(() => {
  return referenceStore.weekdays.map(w => ({
    text: w.name,
    value: w.id
  }))
})

const weekdays = computed(() => {
  return referenceStore.weekdays.sort((a, b) => {
    const orderA = a.day_order || a.id || 0
    const orderB = b.day_order || b.id || 0
    return orderA - orderB
  })
})

const filteredSchedules = computed(() => {
  if (!selectedClassId.value) {
    return []
  }
  return schedules.value
    .filter(s => s.class_id === selectedClassId.value)
    .sort((a, b) => {
      if (a.weekday_id !== b.weekday_id) {
        return a.weekday_id - b.weekday_id
      }
      return a.lesson_number - b.lesson_number
    })
})

const getLessonsForWeekday = (weekdayId) => {
  return filteredSchedules.value.filter(s => s.weekday_id === weekdayId)
}

const onClassChange = () => {
  // При изменении класса автоматически устанавливаем его в форму
  if (selectedClassId.value) {
    form.value.class_id = selectedClassId.value
  }
}

const loadSchedules = async () => {
  loading.value = true
  try {
    const response = await api.get('/schedules')
    schedules.value = response.data || []
  } catch (error) {
    console.error('Ошибка загрузки расписания:', error)
  } finally {
    loading.value = false
  }
}

const openDialog = async (schedule) => {
  // Убеждаемся, что все справочные данные загружены
  if (!referenceStore.classes || referenceStore.classes.length === 0 || 
      !referenceStore.teachers || referenceStore.teachers.length === 0 || 
      !referenceStore.subjects || referenceStore.subjects.length === 0 || 
      !referenceStore.classrooms || referenceStore.classrooms.length === 0 || 
      !referenceStore.weekdays || referenceStore.weekdays.length === 0) {
    await referenceStore.loadAll()
  }
  
  if (schedule) {
    // Находим актуальный объект из списка, чтобы избежать проблем с устаревшими ссылками
    const currentSchedule = schedules.value.find(s => s.id === schedule.id) || schedule
    editingSchedule.value = { ...currentSchedule } // Создаем копию объекта
  } else {
    editingSchedule.value = null
  }
  
  // Открываем диалог
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  // Сбрасываем редактируемое расписание после закрытия диалога
  setTimeout(() => {
    editingSchedule.value = null
    form.value = {
      class_id: selectedClassId.value ? Number(selectedClassId.value) : null,
      weekday_id: null,
      lesson_number: null,
      subject_id: null,
      teacher_id: null,
      classroom_id: null
    }
  }, 300) // Небольшая задержка для анимации закрытия
}

const saveSchedule = async () => {
  try {
    if (editingSchedule.value) {
      await api.put(`/schedules/${editingSchedule.value.id}`, form.value)
    } else {
      await api.post('/schedules', form.value)
    }
    await loadSchedules() // Обновляем список
    closeDialog()
  } catch (error) {
    console.error('Ошибка сохранения расписания:', error)
    alert(error.response?.data?.error || 'Ошибка сохранения')
  }
}

const deleteSchedule = async (id) => {
  if (confirm('Вы уверены, что хотите удалить эту запись расписания?')) {
    try {
      await api.delete(`/schedules/${id}`)
      await loadSchedules()
    } catch (error) {
      console.error('Ошибка удаления расписания:', error)
      alert(error.response?.data?.error || 'Ошибка удаления')
    }
  }
}

// Отслеживаем открытие/закрытие диалога для заполнения/сброса формы
watch(dialog, async (isOpen) => {
  if (isOpen) {
    // Когда диалог открывается, заполняем форму
    await nextTick()
    if (editingSchedule.value) {
      form.value = {
        class_id: editingSchedule.value.class_id ? Number(editingSchedule.value.class_id) : (selectedClassId.value ? Number(selectedClassId.value) : null),
        weekday_id: editingSchedule.value.weekday_id ? Number(editingSchedule.value.weekday_id) : null,
        lesson_number: editingSchedule.value.lesson_number ? Number(editingSchedule.value.lesson_number) : null,
        subject_id: editingSchedule.value.subject_id ? Number(editingSchedule.value.subject_id) : null,
        teacher_id: editingSchedule.value.teacher_id ? Number(editingSchedule.value.teacher_id) : null,
        classroom_id: editingSchedule.value.classroom_id ? Number(editingSchedule.value.classroom_id) : null
      }
    } else {
      // Если редактируемого расписания нет, сбрасываем форму
      form.value = {
        class_id: selectedClassId.value ? Number(selectedClassId.value) : null,
        weekday_id: null,
        lesson_number: null,
        subject_id: null,
        teacher_id: null,
        classroom_id: null
      }
    }
  } else {
    // При закрытии диалога сбрасываем редактируемое расписание через небольшую задержку
    setTimeout(() => {
      editingSchedule.value = null
    }, 300)
  }
})

onMounted(async () => {
  await referenceStore.loadAll()
  await loadSchedules()
})
</script>
