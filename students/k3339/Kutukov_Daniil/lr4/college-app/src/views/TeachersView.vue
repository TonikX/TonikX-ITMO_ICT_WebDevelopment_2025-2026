<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-account-tie" class="mr-2"></v-icon>
          Преподаватели
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
              Добавить преподавателя
            </v-btn>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="teachers"
            :search="search"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.full_name="{ item }">
              {{ item.last_name }} {{ item.first_name }} {{ item.middle_name }}
            </template>
            <template v-slot:item.subjects="{ item }">
              <v-chip v-if="Array.isArray(item.subjects)" class="ma-1" v-for="subject in item.subjects" :key="subject.id" size="small">
                {{ subject.name }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon size="small" @click="editTeacher(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="deleteTeacher(item.id)">
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
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} преподавателя</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedTeacher.last_name"
              label="Фамилия"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedTeacher.first_name"
              label="Имя"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedTeacher.middle_name"
              label="Отчество"
            ></v-text-field>
            <v-select
              v-model="editedTeacher.subjects"
              :items="subjects"
              item-title="name"
              item-value="id"
              label="Предметы"
              multiple
              chips
            ></v-select>
            <v-select
              v-model="editedTeacher.classroom"
              :items="classrooms"
              item-title="number"
              item-value="id"
              label="Кабинет"
              clearable
            ></v-select>
            <v-text-field
              v-model="editedTeacher.phone"
              label="Телефон"
            ></v-text-field>
            <v-text-field
              v-model="editedTeacher.email"
              label="Email"
              type="email"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveTeacher">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collegeService, type Teacher, type Subject } from '@/services/college'

const teachers = ref<Teacher[]>([])
const subjects = ref<Subject[]>([])
const classrooms = ref<any[]>([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editedTeacher = ref<Partial<Teacher>>({
  last_name: '',
  first_name: '',
  middle_name: '',
  subjects: [],
  classroom: null,
  phone: '',
  email: '',
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Предметы', key: 'subjects' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Действия', key: 'actions', sortable: false },
]

onMounted(async () => {
  await loadTeachers()
  await loadSubjects()
  await loadClassrooms()
})

async function loadTeachers() {
  loading.value = true
  try {
    teachers.value = await collegeService.getTeachers()
  } catch (error) {
    console.error('Failed to load teachers:', error)
  } finally {
    loading.value = false
  }
}

async function loadSubjects() {
  try {
    subjects.value = await collegeService.getSubjects()
  } catch (error) {
    console.error('Failed to load subjects:', error)
  }
}

async function loadClassrooms() {
  try {
    classrooms.value = await collegeService.getClassrooms()
  } catch (error) {
    console.error('Failed to load classrooms:', error)
  }
}

function openCreateDialog() {
  editMode.value = false
  editedTeacher.value = {
    last_name: '',
    first_name: '',
    middle_name: '',
    subjects: [],
    classroom: null,
    phone: '',
    email: '',
  }
  dialog.value = true
}

function editTeacher(teacher: Teacher) {
  editMode.value = true
  editedTeacher.value = {
    ...teacher,
    subjects: Array.isArray(teacher.subjects) ? teacher.subjects.map((s: any) => s.id) : [],
    classroom: typeof teacher.classroom === 'object' && teacher.classroom ? teacher.classroom.id : teacher.classroom
  }
  dialog.value = true
}

async function saveTeacher() {
  try {
    if (editMode.value && editedTeacher.value.id) {
      await collegeService.updateTeacher(editedTeacher.value.id, editedTeacher.value)
    } else {
      await collegeService.createTeacher(editedTeacher.value)
    }
    dialog.value = false
    await loadTeachers()
  } catch (error) {
    console.error('Failed to save teacher:', error)
  }
}

async function deleteTeacher(id: number) {
  if (confirm('Удалить преподавателя?')) {
    try {
      await collegeService.deleteTeacher(id)
      await loadTeachers()
    } catch (error) {
      console.error('Failed to delete teacher:', error)
    }
  }
}
</script>
