<script setup lang="ts">
import {ref, computed, onMounted} from "vue"
import {fetchJson} from "../api"

type Applicant = {
  id: number
  full_name: string
  profession: number
  education_level: number
  experience_years: number
  grade: number
  last_salary: string
}

type Profession = { id: number; name: string }
type EducationLevel = { id: number; name: string; rank?: number }

const loading = ref(false)
const error = ref("")

const applicants = ref<Applicant[]>([])
const professions = ref<Profession[]>([])
const educationLevels = ref<EducationLevel[]>([])

const professionById = computed<Record<number, string>>(() => {
  const m: Record<number, string> = {}
  professions.value.forEach(p => (m[p.id] = p.name))
  return m
})

const eduById = computed<Record<number, string>>(() => {
  const m: Record<number, string> = {}
  educationLevels.value.forEach(e => (m[e.id] = e.name))
  return m
})

const rows = computed(() =>
    applicants.value.map(a => ({
      ...a,
      profession_name: professionById.value[a.profession] ?? `#${a.profession}`,
      education_name: eduById.value[a.education_level] ?? `#${a.education_level}`,
    }))
)

const headers = [
  {title: "ID", key: "id"},
  {title: "Full name", key: "full_name"},
  {title: "Profession", key: "profession_name"},
  {title: "Education", key: "education_name"},
  {title: "Experience", key: "experience_years"},
  {title: "Grade", key: "grade"},
  {title: "Last salary", key: "last_salary"},
]

async function loadAll() {
  loading.value = true
  error.value = ""
  try {
    const BASE = "http://127.0.0.1:8000/api"
    const [apps, profs, edus] = await Promise.all([
      fetchJson(`${BASE}/applicants/`),
      fetchJson(`${BASE}/professions/`),
      fetchJson(`${BASE}/education-levels/`),
    ])
    applicants.value = apps
    professions.value = profs
    educationLevels.value = edus
  } catch (e: any) {
    error.value = e?.message ?? String(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      Applicants
      <v-spacer/>
      <v-btn variant="tonal" :loading="loading" @click="loadAll">Reload</v-btn>
    </v-card-title>
    <v-divider/>
    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>

      <v-data-table
          :headers="headers"
          :items="rows"
          density="compact"
          items-per-page="50"
          :footer-props="{
    showFirstLastPage: true
  }"
      />
    </v-card-text>
  </v-card>
</template>
