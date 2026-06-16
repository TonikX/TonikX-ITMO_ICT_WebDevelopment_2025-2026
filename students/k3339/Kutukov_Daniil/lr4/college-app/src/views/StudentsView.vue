<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-account-school" class="mr-2"></v-icon>
          Студенты
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
              Добавить студента
            </v-btn>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="students"
            :search="search"
            :loading="loading"
            class="elevation-1"
          >
            <template v-slot:item.full_name="{ item }">
              {{ item.last_name }} {{ item.first_name }} {{ item.middle_name }}
            </template>
            <template v-slot:item.group="{ item }">
              <v-chip v-if="typeof item.group === 'object'" color="primary">
                {{ item.group.name }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon size="small" @click="editStudent(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="deleteStudent(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog for creating/editing student -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} студента</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedStudent.last_name"
              label="Фамилия"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedStudent.first_name"
              label="Имя"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedStudent.middle_name"
              label="Отчество"
            ></v-text-field>
            <v-select
              v-model="editedStudent.group"
              :items="groups"
              item-title="name"
              item-value="id"
              label="Группа"
              required
            ></v-select>
            <v-text-field
              v-model="editedStudent.enrollment_date"
              label="Дата зачисления"
              type="date"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedStudent.phone"
              label="Телефон"
            ></v-text-field>
            <v-text-field
              v-model="editedStudent.email"
              label="Email"
              type="email"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveStudent">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collegeService, type Student, type Group } from '@/services/college'

const students = ref<Student[]>([])
const groups = ref<Group[]>([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editedStudent = ref<Partial<Student>>({
  last_name: '',
  first_name: '',
  middle_name: '',
  group: 0,
  enrollment_date: '',
  phone: '',
  email: '',
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Группа', key: 'group' },
  { title: 'Дата зачисления', key: 'enrollment_date' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Действия', key: 'actions', sortable: false },
]

onMounted(async () => {
  await loadStudents()
  await loadGroups()
})

async function loadStudents() {
  loading.value = true
  try {
    students.value = await collegeService.getStudents()
  } catch (error) {
    console.error('Failed to load students:', error)
  } finally {
    loading.value = false
  }
}

async function loadGroups() {
  try {
    groups.value = await collegeService.getGroups()
  } catch (error) {
    console.error('Failed to load groups:', error)
  }
}

function openCreateDialog() {
  editMode.value = false
  editedStudent.value = {
    last_name: '',
    first_name: '',
    middle_name: '',
    group: 0,
    enrollment_date: new Date().toISOString().split('T')[0],
    phone: '',
    email: '',
  }
  dialog.value = true
}

function editStudent(student: Student) {
  editMode.value = true
  editedStudent.value = { ...student, group: typeof student.group === 'object' ? student.group.id : student.group }
  dialog.value = true
}

async function saveStudent() {
  try {
    if (editMode.value && editedStudent.value.id) {
      await collegeService.updateStudent(editedStudent.value.id, editedStudent.value)
    } else {
      await collegeService.createStudent(editedStudent.value)
    }
    dialog.value = false
    await loadStudents()
  } catch (error) {
    console.error('Failed to save student:', error)
  }
}

async function deleteStudent(id: number) {
  if (confirm('Удалить студента?')) {
    try {
      await collegeService.deleteStudent(id)
      await loadStudents()
    } catch (error) {
      console.error('Failed to delete student:', error)
    }
  }
}
</script>
