<template>
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Количество учителей по предметам</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="teacherHeaders"
              :items="teachersBySubject"
              :loading="loading"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Количество учеников по полу</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="genderHeaders"
              :items="studentsByGender"
              :loading="loading"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" v-if="false">
        <v-card>
          <v-card-title>Учителя с одинаковыми предметами</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="sameSubjectHeaders"
              :items="teachersBySameSubjects"
              :loading="loading"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Количество кабинетов по типам</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="classroomHeaders"
              :items="classroomsByType"
              :loading="loading"
            ></v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/client'

const loading = ref(false)
const teachersBySubject = ref([])
const studentsByGender = ref([])
const teachersBySameSubjects = ref([])
const classroomsByType = ref([])

const teacherHeaders = [
  { title: 'Предмет', key: 'subject' },
  { title: 'Количество', key: 'count' }
]

const genderHeaders = [
  { title: 'Класс', key: 'class_id' },
  { title: 'Пол', key: 'gender' },
  { title: 'Количество', key: 'count' }
]

const sameSubjectHeaders = [
  { title: 'Учитель 1', key: 'teacher1' },
  { title: 'Учитель 2', key: 'teacher2' },
  { title: 'Предметы', key: 'subjects' }
]

const classroomHeaders = [
  { title: 'Тип', key: 'type' },
  { title: 'Количество', key: 'count' }
]

const loadInfo = async () => {
  loading.value = true
  try {
    const [teachersRes, studentsRes, classroomsRes] = await Promise.all([
      api.get('/info/teachers-count-by-subject').catch(() => ({ data: {} })),
      api.get('/info/students-count-by-gender').catch(() => ({ data: {} })),
      api.get('/info/classrooms-count-by-type').catch(() => ({ data: {} }))
    ])
    
    // Преобразуем map[string]int в массив объектов для таблицы
    teachersBySubject.value = Object.entries(teachersRes.data || {}).map(([subject, count]) => ({
      subject,
      count
    }))
    
    // Преобразуем map[int]map[string]int в массив объектов
    const studentsData = studentsRes.data || {}
    const studentsArray = []
    for (const [classId, genders] of Object.entries(studentsData)) {
      for (const [gender, count] of Object.entries(genders)) {
        studentsArray.push({
          class_id: classId,
          gender: gender === 'M' ? 'Мужской' : gender === 'F' ? 'Женский' : gender,
          count
        })
      }
    }
    studentsByGender.value = studentsArray
    
    // Преобразуем map[string]int в массив объектов
    classroomsByType.value = Object.entries(classroomsRes.data || {}).map(([type, count]) => ({
      type: type === 'basic' ? 'Базовый' : type === 'profile' ? 'Профильный' : type,
      count
    }))
    
    // Учителя с одинаковыми предметами - убираем, так как требует teacherId параметр
    // Можно добавить позже с выбором учителя
    teachersBySameSubjects.value = []
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadInfo()
})
</script>

