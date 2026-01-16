<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-chart-bar" class="mr-2"></v-icon>
          Оценки
        </h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Поиск"
              single-line
              hide-details
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon left>mdi-plus</v-icon>
              Добавить оценку
            </v-btn>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="grades"
            :search="search"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.student="{ item }">
              <span v-if="item.student">
                {{ typeof item.student === 'object' ? `${item.student.last_name} ${item.student.first_name}` : item.student }}
              </span>
            </template>
            <template v-slot:item.subject="{ item }">
              <span v-if="item.subject">
                {{ typeof item.subject === 'object' ? item.subject.name : item.subject }}
              </span>
            </template>
            <template v-slot:item.grade="{ item }">
              <v-chip :color="getGradeColor(item.grade)">
                {{ item.grade }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon size="small" @click="editGrade(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="deleteGrade(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} оценку</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-select
              v-model="editedGrade.student"
              :items="students"
              item-value="id"
              label="Студент"
              required
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="`${item.raw.last_name} ${item.raw.first_name}`"></v-list-item>
              </template>
              <template v-slot:selection="{ item }">
                {{ item.raw.last_name }} {{ item.raw.first_name }}
              </template>
            </v-select>
            <v-select
              v-model="editedGrade.subject"
              :items="subjects"
              item-title="name"
              item-value="id"
              label="Предмет"
              required
            ></v-select>
            <v-select
              v-model="editedGrade.grade"
              :items="[2, 3, 4, 5]"
              label="Оценка"
              required
            ></v-select>
            <v-select
              v-model="editedGrade.semester"
              :items="[1, 2, 3, 4, 5, 6, 7, 8]"
              label="Семестр"
              required
            ></v-select>
            <v-text-field
              v-model="editedGrade.date"
              label="Дата"
              type="date"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveGrade">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collegeService, type Grade, type Student, type Subject } from '@/services/college'

const grades = ref<Grade[]>([])
const students = ref<Student[]>([])
const subjects = ref<Subject[]>([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editedGrade = ref<Partial<Grade>>({
  student: 0,
  subject: 0,
  grade: 5,
  semester: 1,
  date: '',
})

const headers = [
  { title: 'Студент', key: 'student' },
  { title: 'Предмет', key: 'subject' },
  { title: 'Оценка', key: 'grade' },
  { title: 'Семестр', key: 'semester' },
  { title: 'Дата', key: 'date' },
  { title: 'Действия', key: 'actions', sortable: false },
]

onMounted(async () => {
  await loadGrades()
  await loadStudents()
  await loadSubjects()
})

async function loadGrades() {
  loading.value = true
  try {
    grades.value = await collegeService.getGrades()
  } catch (error) {
    console.error('Failed to load grades:', error)
  } finally {
    loading.value = false
  }
}

async function loadStudents() {
  try {
    students.value = await collegeService.getStudents()
  } catch (error) {
    console.error('Failed to load students:', error)
  }
}

async function loadSubjects() {
  try {
    subjects.value = await collegeService.getSubjects()
  } catch (error) {
    console.error('Failed to load subjects:', error)
  }
}

function openCreateDialog() {
  editMode.value = false
  editedGrade.value = {
    student: 0,
    subject: 0,
    grade: 5,
    semester: 1,
    date: new Date().toISOString().split('T')[0],
  }
  dialog.value = true
}

function editGrade(grade: Grade) {
  editMode.value = true
  editedGrade.value = {
    id: grade.id,
    student: typeof grade.student === 'object' ? grade.student.id : grade.student,
    subject: typeof grade.subject === 'object' ? grade.subject.id : grade.subject,
    grade: grade.grade,
    semester: grade.semester,
    date: grade.date,
  }
  dialog.value = true
}

async function saveGrade() {
  try {
    const dataToSend = {
      student: editedGrade.value.student,
      subject: editedGrade.value.subject,
      grade: editedGrade.value.grade,
      semester: editedGrade.value.semester,
      date: editedGrade.value.date,
    }
    
    console.log('Sending grade data:', dataToSend)
    
    if (editMode.value && editedGrade.value.id) {
      await collegeService.updateGrade(editedGrade.value.id, dataToSend)
    } else {
      await collegeService.createGrade(dataToSend)
    }
    dialog.value = false
    await loadGrades()
  } catch (error) {
    console.error('Failed to save grade:', error)
  }
}

async function deleteGrade(id: number) {
  if (confirm('Удалить оценку?')) {
    try {
      await collegeService.deleteGrade(id)
      await loadGrades()
    } catch (error) {
      console.error('Failed to delete grade:', error)
    }
  }
}

function getGradeColor(grade: number): string {
  if (grade === 5) return 'success'
  if (grade === 4) return 'info'
  if (grade === 3) return 'warning'
  return 'error'
}
</script>
