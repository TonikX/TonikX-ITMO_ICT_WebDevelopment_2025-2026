<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>
        <v-icon class="mr-2">mdi-gender-male-female</v-icon>
        Статистика по полу в классах
      </v-toolbar-title>
      <v-spacer />
      <v-btn color="success" @click="loadData" :loading="loading">
        <v-icon left>mdi-refresh</v-icon>
        Обновить
      </v-btn>
    </v-toolbar>

    <v-card-text class="pa-6">
      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate />
        <p class="mt-4">Загрузка статистики...</p>
      </div>

      <div v-else-if="statistics.length > 0">
        <v-row>
          <v-col cols="12" md="8">
            <v-table>
              <thead>
                <tr>
                  <th>Класс</th>
                  <th>Мальчиков</th>
                  <th>Девочек</th>
                  <th>Всего</th>
                  <th>Соотношение</th>
                  <th>Процент мальчиков</th>
                  <th>Процент девочек</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in statistics" :key="item.class_name">
                  <td>
                    <v-chip color="info" variant="flat">
                      {{ item.class_name }}
                    </v-chip>
                  </td>
                  <td>
                    <v-chip color="blue" variant="flat">
                      {{ item.boys_count }}
                    </v-chip>
                  </td>
                  <td>
                    <v-chip color="pink" variant="flat">
                      {{ item.girls_count }}
                    </v-chip>
                  </td>
                  <td>
                    <v-chip color="grey" variant="flat">
                      {{ item.total_students }}
                    </v-chip>
                  </td>
                  <td>
                    <v-progress-linear
                      :model-value="(item.boys_count / item.total_students) * 100"
                      color="blue"
                      height="10"
                      rounded
                    >
                      <template v-slot:default>
                        <span class="text-caption">{{ Math.round((item.boys_count / item.total_students) * 100) }}%</span>
                      </template>
                    </v-progress-linear>
                  </td>
                  <td>
                    {{ ((item.boys_count / item.total_students) * 100).toFixed(1) }}%
                  </td>
                  <td>
                    {{ ((item.girls_count / item.total_students) * 100).toFixed(1) }}%
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>

          <v-col cols="12" md="4">
            <v-card variant="outlined">
              <v-toolbar color="grey-lighten-3" density="compact">
                <v-toolbar-title>Итоговая статистика</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="blue">mdi-gender-male</v-icon>
                    </template>
                    <v-list-item-title>Всего мальчиков</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ totalBoys }}</span>
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="pink">mdi-gender-female</v-icon>
                    </template>
                    <v-list-item-title>Всего девочек</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ totalGirls }}</span>
                    </template>
                  </v-list-item>

                  <v-divider class="my-2" />

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="grey">mdi-account-group</v-icon>
                    </template>
                    <v-list-item-title>Всего учеников</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ totalStudents }}</span>
                    </template>
                  </v-list-item>

                  <v-divider class="my-2" />

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="info">mdi-percent</v-icon>
                    </template>
                    <v-list-item-title>Процент мальчиков</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ percentBoys.toFixed(1) }}%</span>
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon color="info">mdi-percent</v-icon>
                    </template>
                    <v-list-item-title>Процент девочек</v-list-item-title>
                    <template v-slot:append>
                      <span class="text-h6">{{ percentGirls.toFixed(1) }}%</span>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

      </div>

      <div v-else class="text-center py-8">
        <v-icon size="64" color="grey" class="mb-4">mdi-account-group</v-icon>
        <p class="text-h6 text-grey">Статистика не найдена</p>
        <p class="text-body-1 text-grey">Добавьте учеников в систему</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>

export default {
  name: 'GenderReport',
  data() {
    return {
      loading: false,
      statistics: []
    }
  },
  computed: {
    totalBoys() {
      return this.statistics.reduce((sum, item) => sum + item.boys_count, 0)
    },
    totalGirls() {
      return this.statistics.reduce((sum, item) => sum + item.girls_count, 0)
    },
    totalStudents() {
      return this.statistics.reduce((sum, item) => sum + item.total_students, 0)
    },
    percentBoys() {
      return this.totalStudents > 0 ? (this.totalBoys / this.totalStudents) * 100 : 0
    },
    percentGirls() {
      return this.totalStudents > 0 ? (this.totalGirls / this.totalStudents) * 100 : 0
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    notify(type, message) {
      if (this.$toast && typeof this.$toast[type] === 'function') {
        this.$toast[type](message)
      }
    },
    async loadData() {
      this.loading = true
      try {
        const response = await this.$api.reports.getGenderStatistics()
        this.statistics = response.data
        this.notify('success', 'Статистика загружена')
      } catch (error) {
        this.notify('error', 'Ошибка загрузки статистики')
      } finally {
        this.loading = false
      }
    },
  }
}
</script>