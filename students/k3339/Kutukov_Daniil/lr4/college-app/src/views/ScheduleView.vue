<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-4">
          <v-icon icon="mdi-calendar-clock" class="mr-2"></v-icon>
          Расписание
        </h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-select
          v-model="selectedGroup"
          :items="groups"
          item-title="name"
          item-value="id"
          label="Выберите группу"
          @update:model-value="loadSchedule"
        ></v-select>
      </v-col>
      <v-col cols="12" md="7">
        <v-tabs v-model="selectedDay" @update:model-value="loadSchedule">
          <v-tab value="1">Понедельник</v-tab>
          <v-tab value="2">Вторник</v-tab>
          <v-tab value="3">Среда</v-tab>
          <v-tab value="4">Четверг</v-tab>
          <v-tab value="5">Пятница</v-tab>
          <v-tab value="6">Суббота</v-tab>
        </v-tabs>
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary" @click="openCreateDialog" block>
          <v-icon left>mdi-plus</v-icon>
          Добавить
        </v-btn>
      </v-col>
    </v-row>

    <v-row v-if="schedule">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            {{ schedule.group?.name }} - {{ schedule.day_name }}
          </v-card-title>
          <v-card-text>
            <v-timeline side="end" v-if="schedule.lessons && schedule.lessons.length">
              <v-timeline-item
                v-for="lesson in schedule.lessons"
                :key="lesson.id"
                :dot-color="getLessonColor(lesson.lesson_number)"
                size="small"
              >
                <template v-slot:opposite>
                  <div class="text-h6">{{ lesson.start_time }} - {{ lesson.end_time }}</div>
                </template>
                <v-card>
                  <v-card-title>
                    Урок {{ lesson.lesson_number }}: {{ lesson.subject.name }}
                  </v-card-title>
                  <v-card-text>
                    <p>
                      <v-icon>mdi-account-tie</v-icon>
                      {{ lesson.teacher.last_name }} {{ lesson.teacher.first_name.charAt(0) }}.{{ lesson.teacher.middle_name.charAt(0) }}.
                    </p>
                    <p>
                      <v-icon>mdi-door</v-icon>
                      Аудитория: {{ lesson.classroom.number }}
                    </p>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn icon size="small" @click="editSchedule(lesson)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="small" @click="deleteSchedule(lesson.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </v-timeline>
            <p v-else class="text-center text-grey py-8">Нет занятий в этот день</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editMode ? 'Редактировать' : 'Добавить' }} занятие</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-select
              v-model="editedSchedule.group"
              :items="groups"
              item-title="name"
              item-value="id"
              label="Группа"
              required
            ></v-select>
            <v-select
              v-model="editedSchedule.subject"
              :items="subjects"
              item-title="name"
              item-value="id"
              label="Предмет"
              required
            ></v-select>
            <v-select
              v-model="editedSchedule.teacher"
              :items="teachers"
              item-value="id"
              label="Преподаватель"
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
              v-model="editedSchedule.classroom"
              :items="classrooms"
              item-title="number"
              item-value="id"
              label="Аудитория"
              required
            ></v-select>
            <v-select
              v-model="editedSchedule.day_of_week"
              :items="dayOptions"
              item-title="name"
              item-value="value"
              label="День недели"
              required
            ></v-select>
            <v-select
              v-model="editedSchedule.lesson_number"
              :items="[1, 2, 3, 4, 5, 6, 7, 8]"
              label="Номер пары"
              required
            ></v-select>
            <v-text-field
              v-model="editedSchedule.start_time"
              label="Время начала"
              type="time"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedSchedule.end_time"
              label="Время окончания"
              type="time"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveSchedule">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collegeService, type Group, type Schedule, type Subject, type Teacher } from '@/services/college'

const groups = ref<Group[]>([])
const subjects = ref<Subject[]>([])
const teachers = ref<Teacher[]>([])
const classrooms = ref<any[]>([])
const selectedGroup = ref<number | null>(null)
const selectedDay = ref('1')
const schedule = ref<any>(null)
const dialog = ref(false)
const editMode = ref(false)
const editedSchedule = ref<Partial<Schedule>>({
  group: 0,
  subject: 0,
  teacher: 0,
  classroom: 0,
  day_of_week: 1,
  lesson_number: 1,
  start_time: '09:00',
  end_time: '10:30',
})

const lessonColors = ['primary', 'success', 'info', 'warning', 'error', 'purple']
const dayOptions = [
  { name: 'Понедельник', value: 1 },
  { name: 'Вторник', value: 2 },
  { name: 'Среда', value: 3 },
  { name: 'Четверг', value: 4 },
  { name: 'Пятница', value: 5 },
  { name: 'Суббота', value: 6 },
]

onMounted(async () => {
  await loadGroups()
  await loadSubjects()
  await loadTeachers()
  await loadClassrooms()
})

async function loadGroups() {
  try {
    groups.value = await collegeService.getGroups()
    if (groups.value.length > 0) {
      selectedGroup.value = groups.value[0].id
      await loadSchedule()
    }
  } catch (error) {
    console.error('Failed to load groups:', error)
  }
}

async function loadSubjects() {
  try {
    subjects.value = await collegeService.getSubjects()
  } catch (error) {
    console.error('Failed to load subjects:', error)
  }
}

async function loadTeachers() {
  try {
    teachers.value = await collegeService.getTeachers()
  } catch (error) {
    console.error('Failed to load teachers:', error)
  }
}

async function loadClassrooms() {
  try {
    classrooms.value = await collegeService.getClassrooms()
  } catch (error) {
    console.error('Failed to load classrooms:', error)
  }
}

async function loadSchedule() {
  if (!selectedGroup.value) return

  try {
    schedule.value = await collegeService.getGroupDaySchedule(
      selectedGroup.value,
      Number(selectedDay.value)
    )
  } catch (error) {
    console.error('Failed to load schedule:', error)
  }
}

function openCreateDialog() {
  editMode.value = false
  editedSchedule.value = {
    group: selectedGroup.value || 0,
    subject: 0,
    teacher: 0,
    classroom: 0,
    day_of_week: Number(selectedDay.value),
    lesson_number: 1,
    start_time: '09:00',
    end_time: '10:30',
  }
  dialog.value = true
}

function editSchedule(lesson: any) {
  editMode.value = true
  editedSchedule.value = {
    ...lesson,
    group: typeof lesson.group === 'object' ? lesson.group.id : lesson.group,
    subject: typeof lesson.subject === 'object' ? lesson.subject.id : lesson.subject,
    teacher: typeof lesson.teacher === 'object' ? lesson.teacher.id : lesson.teacher,
    classroom: typeof lesson.classroom === 'object' ? lesson.classroom.id : lesson.classroom,
  }
  dialog.value = true
}

async function saveSchedule() {
  try {
    const dataToSend = {
      group: editedSchedule.value.group,
      subject: editedSchedule.value.subject,
      teacher: editedSchedule.value.teacher,
      classroom: editedSchedule.value.classroom,
      day_of_week: editedSchedule.value.day_of_week,
      lesson_number: editedSchedule.value.lesson_number,
      start_time: editedSchedule.value.start_time,
      end_time: editedSchedule.value.end_time,
    }
    
    if (editMode.value && editedSchedule.value.id) {
      await collegeService.updateSchedule(editedSchedule.value.id, dataToSend)
    } else {
      await collegeService.createSchedule(dataToSend)
    }
    dialog.value = false
    await loadSchedule()
  } catch (error) {
    console.error('Failed to save schedule:', error)
  }
}

async function deleteSchedule(id: number) {
  if (confirm('Удалить занятие из расписания?')) {
    try {
      await collegeService.deleteSchedule(id)
      await loadSchedule()
    } catch (error) {
      console.error('Failed to delete schedule:', error)
    }
  }
}

function getLessonColor(lessonNumber: number): string {
  return lessonColors[(lessonNumber - 1) % lessonColors.length]
}
</script>
