<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-account-group" class="mr-2"></v-icon>
          Группы
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
              Добавить группу
            </v-btn>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="groups"
            :search="search"
            :loading="loading"
            @click:row="viewGroup"
            class="elevation-1"
          >
            <template v-slot:item.course="{ item }">
              <v-chip color="primary">{{ item.course }} курс</v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn icon size="small" @click.stop="editGroup(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon size="small" @click.stop="deleteGroup(item.id)">
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
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} группу</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedGroup.name"
              label="Название"
              required
            ></v-text-field>
            <v-select
              v-model="editedGroup.course"
              :items="[1, 2, 3, 4]"
              label="Курс"
              required
            ></v-select>
            <v-text-field
              v-model="editedGroup.specialty"
              label="Специальность"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveGroup">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { collegeService, type Group } from '@/services/college'

const router = useRouter()
const groups = ref<Group[]>([])
const loading = ref(false)
const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editedGroup = ref<Partial<Group>>({
  name: '',
  course: 1,
  specialty: '',
})

const headers = [
  { title: 'Название', key: 'name' },
  { title: 'Курс', key: 'course' },
  { title: 'Специальность', key: 'specialty' },
  { title: 'Действия', key: 'actions', sortable: false },
]

onMounted(async () => {
  await loadGroups()
})

async function loadGroups() {
  loading.value = true
  try {
    groups.value = await collegeService.getGroups()
  } catch (error) {
    console.error('Failed to load groups:', error)
  } finally {
    loading.value = false
  }
}

function viewGroup(event: any, row: any) {
  router.push(`/groups/${row.item.id}`)
}

function openCreateDialog() {
  editMode.value = false
  editedGroup.value = {
    name: '',
    course: 1,
    specialty: '',
  }
  dialog.value = true
}

function editGroup(group: Group) {
  editMode.value = true
  editedGroup.value = { ...group }
  dialog.value = true
}

async function saveGroup() {
  try {
    if (editMode.value && editedGroup.value.id) {
      await collegeService.updateGroup(editedGroup.value.id, editedGroup.value)
    } else {
      await collegeService.createGroup(editedGroup.value)
    }
    dialog.value = false
    await loadGroups()
  } catch (error) {
    console.error('Failed to save group:', error)
  }
}

async function deleteGroup(id: number) {
  if (confirm('Удалить группу?')) {
    try {
      await collegeService.deleteGroup(id)
      await loadGroups()
    } catch (error) {
      console.error('Failed to delete group:', error)
    }
  }
}
</script>
