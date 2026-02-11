<template>
  <div>
    <h1 class="text-h4 font-weight-bold mb-6">Журнал преподавателя</h1>

    <v-card border>
      <v-table>
        <thead>
          <tr>
            <th class="text-left">ID</th>
            <th class="text-left">Студент</th>
            <th class="text-left">Задание / Вариант</th>
            <th class="text-left">Рецензии (Оценки)</th>
            <th class="text-left">Средний балл</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in submissions" :key="sub.id">
            <td>#{{ sub.id }}</td>
            <td>
              <v-chip size="small" color="primary" variant="outlined">
                Student ID: {{ sub.student }}
              </v-chip>
            </td>
            <td>
              <div class="text-caption text-medium-emphasis">
                {{ sub.variant ? sub.variant.description : 'Без варианта' }}
              </div>
              <div class="text-truncate" style="max-width: 250px;">
                <a :href="sub.content" target="_blank" class="text-decoration-none text-white">
                  {{ sub.content }}
                </a>
              </div>
            </td>
            <td>
              <div v-if="getReviewsFor(sub.id).length > 0" class="d-flex gap-2 flex-wrap py-2">
                <v-tooltip location="top" v-for="rev in getReviewsFor(sub.id)" :key="rev.id">
                  <template v-slot:activator="{ props }">
                    <v-chip v-bind="props" size="small" color="secondary">
                      {{ rev.total_score }}
                    </v-chip>
                  </template>
                  <span>{{ rev.comments }} (от User {{ rev.reviewer }})</span>
                </v-tooltip>
              </div>
              <span v-else class="text-caption text-disabled">Нет проверок</span>
            </td>
            <td>
              <strong :class="getAvgScore(sub.id) >= 4 ? 'text-success' : 'text-warning'">
                {{ getAvgScore(sub.id) }}
              </strong>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({ 
    submissions: [],
    reviews: []
  }),
  
  async mounted() {
    this.loadData();
  },

  methods: {
    async loadData() {
      const token = localStorage.getItem('auth_token');
      const config = { headers: { Authorization: `Token ${token}` } };
      
      try {
        const [subRes, revRes] = await Promise.all([
          axios.get('http://127.0.0.1:8000/api/submissions/', config),
          axios.get('http://127.0.0.1:8000/api/reviews/', config)
        ]);

        this.submissions = subRes.data;
        this.reviews = revRes.data;
      } catch (e) {
        console.error("Ошибка загрузки журнала", e);
      }
    },

    getReviewsFor(submissionId) {
      return this.reviews.filter(r => r.submission === submissionId);
    },

    getAvgScore(submissionId) {
      const revs = this.getReviewsFor(submissionId);
      if (revs.length === 0) return '-';
      const sum = revs.reduce((acc, curr) => acc + curr.total_score, 0);
      return (sum / revs.length).toFixed(1);
    }
  }
}
</script>