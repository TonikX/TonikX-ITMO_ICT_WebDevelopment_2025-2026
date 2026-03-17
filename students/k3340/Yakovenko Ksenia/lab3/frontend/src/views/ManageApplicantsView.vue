<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { fetchJson, apiFetchJson } from "../api"

type Applicant = {
  id: number
  full_name: string
  profession: number
  education_level: number
  experience_years: number
  grade: number
  last_salary: number
}

type Profession = {
  id: number
  name: string
}

type EducationLevel = {
  id: number
  name: string
}

const loading = ref(false)
const saving = ref(false)
const error = ref("")
const success = ref("")

const applicants = ref<Applicant[]>([])
const professions = ref<Profession[]>([])
const educationLevels = ref<EducationLevel[]>([])

const dialog = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)

const form = ref({
  full_name: "",
  profession: null as number | null,
  education_level: null as number | null,
  experience_years: 0,
  grade: 1,
  last_salary: 0,
})

const headers = [
  { title: "ID", key: "id" },
  { title: "Full name", key: "full_name" },
  { title: "Profession", key: "profession_name" },
  { title: "Education", key: "education_name" },
  { title: "Experience", key: "experience_years" },
  { title: "Grade", key: "grade" },
  { title: "Last salary", key: "last_salary" },
  { title: "Actions", key: "actions", sortable: false },
]

const professionById = computed<Record<number, string>>(() => {
  const m: Record<number, string> = {}
  professions.value.forEach((p) => (m[p.id] = p.name))
  return m
})

const eduById = computed<Record<number, string>>(() => {
  const m: Record<number, string> = {}
  educationLevels.value.forEach((e) => (m[e.id] = e.name))
  return m
})

const rows = computed(() =>
  applicants.value.map((a) => ({
    ...a,
    profession_name: professionById.value[a.profession] ?? `#${a.profession}`,
    education_name: eduById.value[a.education_level] ?? `#${a.education_level}`,
  }))
)

function resetForm() {
  form.value = {
    full_name: "",
    profession: null,
    education_level: null,
    experience_years: 0,
    grade: 1,
    last_salary: 0,
  }
  editingId.value = null
  isEdit.value = false
}

function openCreateDialog() {
  resetForm()
  dialog.value = true
}

function openEditDialog(item: any) {
  const a = item.raw ?? item

  isEdit.value = true
  editingId.value = a.id

  form.value = {
    full_name: a.full_name,
    profession: a.profession,
    education_level: a.education_level,
    experience_years: a.experience_years,
    grade: a.grade,
    last_salary: Number(a.last_salary),
  }

  dialog.value = true
}

async function loadAll() {
  loading.value = true
  error.value = ""
  success.value = ""

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

async function saveApplicant() {
  saving.value = true
  error.value = ""
  success.value = ""

  try {
    const payload = {
      full_name: form.value.full_name,
      profession: form.value.profession,
      education_level: form.value.education_level,
      experience_years: Number(form.value.experience_years),
      grade: Number(form.value.grade),
      last_salary: Number(form.value.last_salary),
    }

    if (isEdit.value && editingId.value !== null) {
      await apiFetchJson(`/applicants/${editingId.value}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      success.value = "Applicant updated"
    } else {
      await apiFetchJson("/applicants/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      success.value = "Applicant created"
    }

    dialog.value = false
    resetForm()
    await loadAll()
  } catch (e: any) {
    error.value = e?.message ?? String(e)
  } finally {
    saving.value = false
  }
}

async function deleteApplicant(id: number) {
  const ok = window.confirm("Delete applicant?")
  if (!ok) return

  try {
    await apiFetchJson(`/applicants/${id}/`, {
      method: "DELETE",
    })

    success.value = "Applicant deleted"
    await loadAll()
  } catch (e: any) {
    error.value = e?.message ?? String(e)
  }
}

onMounted(loadAll)
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      Manage Applicants
      <v-spacer />
      <v-btn color="primary" @click="openCreateDialog">Add Applicant</v-btn>
      <v-btn class="ml-2" variant="tonal" @click="loadAll">Reload</v-btn>
    </v-card-title>

    <v-divider />

    <v-card-text>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">
        {{ error }}
      </v-alert>

      <v-alert v-if="success" type="success" variant="tonal" class="mb-3">
        {{ success }}
      </v-alert>

      <v-data-table
        :headers="headers"
        :items="rows"
        :loading="loading"
        items-per-page="10"
        density="compact"
      >
        <template #item.actions="{ item }">
  <div style="display: flex; gap: 8px; flex-wrap: nowrap;">
    <v-btn
      size="small"
      variant="tonal"
      @click="openEditDialog(item.raw ?? item)"
    >
      Edit
    </v-btn>

    <v-btn
      size="small"
      color="red"
      variant="tonal"
      @click="deleteApplicant((item.raw ?? item).id)"
    >
      Delete
    </v-btn>
  </div>
</template>
      </v-data-table>
    </v-card-text>
  </v-card>

  <v-dialog v-model="dialog" max-width="700">
    <v-card>
      <v-card-title>
        {{ isEdit ? "Edit Applicant" : "Add Applicant" }}
      </v-card-title>

      <v-card-text>
        <v-text-field v-model="form.full_name" label="Full name" />

        <v-select
          v-model="form.profession"
          :items="professions"
          item-title="name"
          item-value="id"
          label="Profession"
        />

        <v-select
          v-model="form.education_level"
          :items="educationLevels"
          item-title="name"
          item-value="id"
          label="Education level"
        />

        <v-text-field v-model="form.experience_years" label="Experience years" type="number" />

        <v-text-field v-model="form.grade" label="Grade" type="number" />

        <v-text-field v-model="form.last_salary" label="Last salary" type="number" />
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :loading="saving" @click="saveApplicant">
          {{ isEdit ? "Save changes" : "Create" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>