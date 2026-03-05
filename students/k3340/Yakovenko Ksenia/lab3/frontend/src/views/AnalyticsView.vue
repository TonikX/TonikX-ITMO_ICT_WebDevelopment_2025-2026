<script setup lang="ts">
import {ref, computed} from "vue"
import {fetchJson} from "../api"

type Endpoint = { key: string; title: string; url: string }

const BASE = "http://127.0.0.1:8000/api"

const endpoints: Endpoint[] = [
  {key: "benefits", title: "Active benefits count", url: `${BASE}/analytics/active-benefits-count/`},
  {
    key: "open_days",
    title: "Open vacancies days since posted",
    url: `${BASE}/analytics/open-vacancies-days-since-posted/`
  },
  {
    key: "prof_missing",
    title: "Applicant professions not in vacancies",
    url: `${BASE}/analytics/applicant-professions-not-in-vacancies/`
  },
  {key: "vac_for_app", title: "Vacancies for applicants", url: `${BASE}/analytics/vacancies-for-applicants/`},
  {
    key: "count_range",
    title: "Vacancies count (high edu + salary range)",
    url: `${BASE}/analytics/vacancies-count-high-edu-salary-range/`
  },
]

const selected = ref<Endpoint>(endpoints[1])
const loading = ref(false)
const error = ref("")
const result = ref<any>(null)

const isArray = computed(() => Array.isArray(result.value))
const isObject = computed(() => result.value && typeof result.value === "object" && !Array.isArray(result.value))

const isVacanciesForApplicants = computed(() => selected.value?.key === "vac_for_app")

const tableHeaders = computed(() => {
  if (!Array.isArray(result.value) || result.value.length === 0) return []
  const first = result.value[0]
  if (!first || typeof first !== "object" || Array.isArray(first)) return []
  return Object.keys(first).map(k => ({title: k, key: k}))
})

const vacancyHeaders = [
  {title: "ID", key: "id"},
  {title: "Employer", key: "employer"},
  {title: "Profession", key: "profession"},
  {title: "Education", key: "education_required"},
  {title: "Experience", key: "required_experience_years"},
  {title: "Grade", key: "required_grade"},
  {title: "Salary", key: "salary"},
  {title: "Status", key: "status"},
  {title: "Posted", key: "date_posted"},
]

function normalizeVacancy(v: any) {
  return {...v, salary: `${v.salary_from}–${v.salary_to}`}
}

async function run(ep: Endpoint = selected.value) {
  selected.value = ep
  loading.value = true
  error.value = ""
  result.value = null
  try {
    result.value = await fetchJson(ep.url)
  } catch (e: any) {
    error.value = e?.message ?? String(e)
  } finally {
    loading.value = false
  }
}

// сразу грузим выбранный эндпоинт
run(selected.value)
</script>

<template>
  <div>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h4">Analytics</h1>
      <v-spacer/>
      <v-chip v-if="selected" color="primary" variant="tonal">{{ selected.title }}</v-chip>
    </div>

    <v-row>
      <!-- Слева список -->
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Requests</v-card-title>
          <v-divider/>
          <v-list density="comfortable">
            <v-list-item
                v-for="ep in endpoints"
                :key="ep.key"
                :active="selected?.key === ep.key"
                @click="run(ep)"
            >
              <v-list-item-title>{{ ep.title }}</v-list-item-title>
              <v-list-item-subtitle class="text-truncate">{{ ep.url }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Справа результат -->
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="d-flex align-center">
            Result
            <v-spacer/>
            <v-btn variant="tonal" :loading="loading" @click="run(selected)">Refresh</v-btn>
          </v-card-title>
          <v-divider/>

          <v-card-text>
            <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>
            <v-skeleton-loader v-if="loading" type="paragraph, paragraph, paragraph"/>

            <!-- Спец-вид для сложного эндпоинта -->
            <div v-else-if="isVacanciesForApplicants && Array.isArray(result)">
              <v-expansion-panels variant="accordion">
                <v-expansion-panel v-for="row in result" :key="row.applicant?.id">
                  <v-expansion-panel-title>
                    <div class="d-flex align-center" style="gap: 12px; flex-wrap: wrap;">
                      <strong>{{ row.applicant?.full_name }}</strong>
                      <v-chip size="small" variant="tonal">exp: {{ row.applicant?.experience_years }}</v-chip>
                      <v-chip size="small" variant="tonal">grade: {{ row.applicant?.grade }}</v-chip>
                      <v-chip size="small" color="primary" variant="tonal">
                        matches: {{ row.vacancies?.length ?? 0 }}
                      </v-chip>
                    </div>
                  </v-expansion-panel-title>

                  <v-expansion-panel-text>
                    <v-alert v-if="!row.vacancies || row.vacancies.length === 0" type="info" variant="tonal">
                      No suitable vacancies found for this applicant.
                    </v-alert>

                    <v-data-table
                        v-else
                        :headers="vacancyHeaders"
                        :items="row.vacancies.map(normalizeVacancy)"
                        density="compact"
                        items-per-page="10"
                    />
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>

            <!-- Массив объектов: таблица -->
            <div v-else-if="isArray && tableHeaders.length">
              <v-data-table
                  :headers="tableHeaders"
                  :items="result"
                  density="compact"
                  items-per-page="50"
                  class="bg-white"
                  :footer-props="{
    showFirstLastPage: true
  }"
              />
            </div>

            <!-- Объект: key/value -->
            <div v-else-if=" isObject
              ">
              <v-table density="compact">
                <tbody>
                <tr v-for="(v, k) in result" :key="k">
                  <td style="width: 40%"><strong>{{ k }}</strong></td>
                  <td>{{ v }}</td>
                </tr>
                </tbody>
              </v-table>
            </div>

            <!-- Иначе: JSON -->
            <div v-else-if="result !== null">
              <v-card variant="tonal">
                <v-card-text
                    style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; white-space: pre-wrap;">
                  {{ JSON.stringify(result, null, 2) }}
                </v-card-text>
              </v-card>
            </div>

            <div v-else class="text-medium-emphasis">
              Select a request from the left panel.
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>