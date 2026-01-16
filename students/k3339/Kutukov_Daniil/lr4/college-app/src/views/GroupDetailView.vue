<template>
  <v-container v-if="group">
    <v-row>
      <v-col cols="12">
        <v-btn icon @click="router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <h1 class="text-h3 mb-4 d-inline-block ml-4">
          {{ group.name }}
        </h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Информация о группе</v-card-title>
          <v-card-text>
            <p><strong>Курс:</strong> {{ group.course }}</p>
            <p><strong>Специальность:</strong> {{ group.specialty }}</p>
            <p><strong>Количество студентов:</strong> {{ group.students_count || 'Загрузка...' }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Расписание на неделю</v-card-title>
          <v-card-text>
            <v-tabs v-model="selectedDay">
              <v-tab value="1">Пн</v-tab>
              <v-tab value="2">Вт</v-tab>
              <v-tab value="3">Ср</v-tab>
              <v-tab value="4">Чт</v-tab>
              <v-tab value="5">Пт</v-tab>
              <v-tab value="6">Сб</v-tab>
            </v-tabs>

            <v-window v-model="selectedDay">
              <v-window-item v-for="day in [1,2,3,4,5,6]" :key="day" :value="String(day)">
                <v-card flat>
                  <v-card-text>
                    <v-list v-if="daySchedule && daySchedule.lessons?.length">
                      <v-list-item v-for="lesson in daySchedule.lessons" :key="lesson.id">
                        <v-list-item-title>
                          {{ lesson.lesson_number }}. {{ lesson.subject.name }}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ lesson.teacher.last_name }} {{ lesson.teacher.first_name.charAt(0) }}.{{ lesson.teacher.middle_name.charAt(0) }}. - 
                          Ауд. {{ lesson.classroom.number }}
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                    <p v-else class="text-center text-grey">Нет занятий</p>
                  </v-card-text>
                </v-card>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <span>Ведомость успеваемости</span>
            <v-spacer></v-spacer>
            <v-select
              v-model="selectedSemester"
              :items="[1,2,3,4,5,6,7,8]"
              label="Семестр"
              style="max-width: 150px"
              @update:model-value="loadGradeSheet"
            ></v-select>
          </v-card-title>
          <v-card-text>
            <div v-if="gradeSheet && gradeSheet.students">
              <v-expansion-panels>
                <v-expansion-panel v-for="studentData in gradeSheet.students" :key="studentData.student.id">
                  <v-expansion-panel-title>
                    {{ studentData.student.last_name }} {{ studentData.student.first_name }} {{ studentData.student.middle_name }}
                    <v-spacer></v-spacer>
                    <v-chip color="primary">Средний балл: {{ studentData.average?.toFixed(2) || '-' }}</v-chip>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-list>
                      <v-list-item v-for="subject in studentData.subjects" :key="subject.subject.id">
                        <v-list-item-title>{{ subject.subject.name }}</v-list-item-title>
                        <v-list-item-subtitle>
                          Оценки: {{ subject.grades.join(', ') }} | Средний балл: {{ subject.average?.toFixed(2) }}
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { collegeService } from '@/services/college'

const route = useRoute()
const router = useRouter()
const group = ref<any>(null)
const daySchedule = ref<any>(null)
const gradeSheet = ref<any>(null)
const selectedDay = ref('1')
const selectedSemester = ref(1)

onMounted(async () => {
  const id = Number(route.params.id)
  await loadGroup(id)
  await loadDaySchedule(id, 1)
  await loadGradeSheet()
})

watch(selectedDay, async (newDay) => {
  const id = Number(route.params.id)
  await loadDaySchedule(id, Number(newDay))
})

async function loadGroup(id: number) {
  try {
    group.value = await collegeService.getGroup(id)
  } catch (error) {
    console.error('Failed to load group:', error)
  }
}

async function loadDaySchedule(groupId: number, day: number) {
  try {
    daySchedule.value = await collegeService.getGroupDaySchedule(groupId, day)
  } catch (error) {
    console.error('Failed to load schedule:', error)
  }
}

async function loadGradeSheet() {
  const id = Number(route.params.id)
  try {
    gradeSheet.value = await collegeService.getGradeSheet(id, selectedSemester.value)
  } catch (error) {
    console.error('Failed to load grade sheet:', error)
  }
}
</script>
