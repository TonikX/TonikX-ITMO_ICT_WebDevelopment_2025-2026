<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Главная панель</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-card class="text-center" color="primary" dark>
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-newspaper-variant</v-icon>
            <div class="text-h5">{{ stats.newspapers }}</div>
            <div class="text-body-2">Газет</div>
          </v-card-text>
          <v-card-actions>
            <v-btn block variant="text" to="/newspapers">
              Перейти к газетам
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="text-center" color="secondary" dark>
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-printer</v-icon>
            <div class="text-h5">{{ stats.printingHouses }}</div>
            <div class="text-body-2">Типографий</div>
          </v-card-text>
          <v-card-actions>
            <v-btn block variant="text" to="/printing-houses">
              Перейти к типографиям
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="text-center" color="success" dark>
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-email</v-icon>
            <div class="text-h5">{{ stats.postOffices }}</div>
            <div class="text-body-2">Почтовых отделений</div>
          </v-card-text>
          <v-card-actions>
            <v-btn block variant="text" to="/post-offices">
              Перейти к почтовым отделениям
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="text-center" color="info" dark>
          <v-card-text>
            <v-icon size="48" class="mb-2">mdi-truck-delivery</v-icon>
            <div class="text-h5">{{ stats.distributions }}</div>
            <div class="text-body-2">Распределений</div>
          </v-card-text>
          <v-card-actions>
            <v-btn block variant="text" to="/distributions">
              Перейти к распределениям
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Быстрые действия</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  color="primary"
                  size="large"
                  prepend-icon="mdi-plus"
                  to="/newspapers?action=create"
                >
                  Создать газету
                </v-btn>
              </v-col>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  color="primary"
                  size="large"
                  prepend-icon="mdi-plus"
                  to="/printing-houses?action=create"
                >
                  Создать типографию
                </v-btn>
              </v-col>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  color="primary"
                  size="large"
                  prepend-icon="mdi-plus"
                  to="/post-offices?action=create"
                >
                  Создать почтовое отделение
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Отчеты</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-btn
                  block
                  variant="outlined"
                  prepend-icon="mdi-file-document"
                  @click="loadReport"
                  :loading="loadingReport"
                >
                  Отчет о работе типографий
                </v-btn>
              </v-col>
            </v-row>
            <v-row v-if="reportData.length > 0" class="mt-4">
              <v-col cols="12">
                <v-expansion-panels>
                  <v-expansion-panel
                    v-for="(item, index) in reportData"
                    :key="index"
                  >
                    <v-expansion-panel-title>
                      {{ item.printing_house.name }} ({{ item.total_newspapers }} газет)
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                      <div v-for="(newspaper, nIndex) in item.newspapers" :key="nIndex" class="mb-2">
                        <strong>{{ newspaper.newspaper }}</strong> - тираж: {{ newspaper.circulation }},
                        распределено: {{ newspaper.total_distributed }}
                      </div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const stats = ref({
  newspapers: 0,
  printingHouses: 0,
  postOffices: 0,
  distributions: 0,
})

const reportData = ref<{
  printing_house: {
    name: string
  }
  total_newspapers: number
  newspapers: {
    newspaper: string
    circulation: number
    total_distributed: number
  }[]
}[]>([])
const loadingReport = ref(false)

async function loadStats() {
  try {
    const [newspapers, printingHouses, postOffices, distributions] = await Promise.all([
      api.getNewspapers({ page_size: 1 }),
      api.getPrintingHouses({ page_size: 1 }),
      api.getPostOffices({ page_size: 1 }),
      api.getDistributions({ page_size: 1 }),
    ])

    stats.value = {
      newspapers: newspapers.count || 0,
      printingHouses: printingHouses.count || 0,
      postOffices: postOffices.count || 0,
      distributions: distributions.count || 0,
    }
  } catch {
    console.error('Ошибка загрузки статистики')
  }
}

async function loadReport() {
  loadingReport.value = true
  try {
    const data = await api.getPrintingHousesReport()
    reportData.value = data
  } catch {
    console.error('Ошибка загрузки отчета')
  } finally {
    loadingReport.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>
