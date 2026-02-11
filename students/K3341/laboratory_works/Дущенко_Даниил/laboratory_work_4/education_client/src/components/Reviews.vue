<template>
  <v-container>
    <h1 class="text-h4 font-weight-bold mb-6">Взаимная проверка (Peer Review)</h1>

    <v-row>

      <v-col cols="12" md="7">
        <v-card class="pa-0" border>
          <v-toolbar color="surface" density="compact">
            <v-toolbar-title class="text-subtitle-1">Доступные решения</v-toolbar-title>
          </v-toolbar>
          
          <v-table hover>
            <thead>
              <tr>
                <th class="text-left">ID</th>
                <th class="text-left">Студент</th>
                <th class="text-left">Вариант</th>
                <th class="text-left">Действие</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sub in submissions" :key="sub.id" :class="{'bg-primary-lighten-5': sub.id === selectedId}">
                <td>#{{ sub.id }}</td>
                <td>Student {{ sub.student }}</td> 
                <td>
                  <div class="text-truncate" style="max-width: 200px;">
                    {{ sub.variant ? sub.variant.description : 'Вариант удален' }}
                  </div>
                </td>
                <td>
                  <v-btn 
                    size="small" 
                    variant="tonal" 
                    color="secondary"
                    @click="selectSubmission(sub)"
                  >
                    Проверить
                  </v-btn>
                </td>
              </tr>
              <tr v-if="submissions.length === 0">
                <td colspan="4" class="text-center pa-4 text-medium-emphasis">
                  Нет решений для проверки
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>

      <v-col cols="12" md="5">
        <v-card class="pa-6 sticky-top" elevation="3" style="position: sticky; top: 20px;">
          <h2 class="text-h6 mb-4 d-flex align-center">
            <v-icon icon="mdi-fountain-pen-tip" color="secondary" class="mr-3"></v-icon>
            Оценка работы #{{ selectedId || '...' }}
          </h2>

          <v-alert v-if="selectedContent" type="info" variant="tonal" class="mb-4 text-caption" border="start">
            <strong>Решение студента:</strong><br>
            {{ selectedContent }}
          </v-alert>

          <v-text-field 
            v-model="score" 
            label="Балл (1-5)" 
            type="number" 
            prepend-inner-icon="mdi-star"
            variant="outlined"
            :disabled="!selectedId"
          ></v-text-field>
          
          <v-textarea 
            v-model="comment" 
            label="Комментарий к работе" 
            placeholder="Что сделано хорошо, а что плохо?"
            rows="5"
            variant="outlined"
            :disabled="!selectedId"
          ></v-textarea>
          
          <v-btn 
            block color="secondary" size="large" class="mt-4" 
            @click="sendReview"
            :disabled="!selectedId"
          >
            Сохранить рецензию
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({ 
    submissions: [], 
    selectedId: null, 
    selectedContent: '',
    comment: '', 
    score: '' 
  }),
  
  async mounted() {
    this.loadSubmissions();
  },

  methods: {
    async loadSubmissions() {
      const token = localStorage.getItem('auth_token');
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/submissions/', {
          headers: { Authorization: `Token ${token}` }
        });
        this.submissions = res.data;
      } catch (e) {
        console.error(e);
      }
    },

    selectSubmission(sub) {
      this.selectedId = sub.id;
      this.selectedContent = sub.content; 
      if (window.innerWidth < 960) {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }
    },

    async sendReview() {
      if (!this.selectedId) return;
      
      const token = localStorage.getItem('auth_token');
      try {
        await axios.post('http://127.0.0.1:8000/api/reviews/', 
          { submission: this.selectedId, comments: this.comment, total_score: this.score },
          { headers: { Authorization: `Token ${token}` } }
        );
        alert('Рецензия сохранена!');
        this.comment = '';
        this.score = '';
        this.selectedId = null;
        this.selectedContent = '';
      } catch (e) {
        alert('Ошибка сохранения');
      }
    }
  }
}
</script>

<style scoped>
.bg-primary-lighten-5 {
  background-color: rgba(16, 185, 129, 0.1) !important; 
}
</style>