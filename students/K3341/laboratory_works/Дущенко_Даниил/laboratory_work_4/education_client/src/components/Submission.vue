<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="5">
        <v-card class="pa-6" elevation="3">
          <h2 class="text-h5 mb-6 d-flex align-center">
            <v-icon icon="mdi-upload" color="primary" class="mr-3"></v-icon>
            Сдать новую работу
          </h2>

          <v-select 
            v-model="selectedVariant" 
            :items="variants" 
            item-title="label" 
            item-value="id"
            label="Выберите задание и вариант"
            prepend-inner-icon="mdi-format-list-bulleted"
            no-data-text="Нет доступных заданий"
            variant="outlined"
          ></v-select>
          
          <v-textarea 
            v-model="content" 
            label="Ссылка на GitHub или текст решения"
            prepend-inner-icon="mdi-link"
            rows="4"
            variant="outlined"
            class="mt-3"
          ></v-textarea>
          
          <v-btn 
            block color="primary" size="large" class="mt-6" 
            @click="submitWork" 
            :loading="loading"
          >
            Отправить
          </v-btn>
        </v-card>
      </v-col>

      <v-col cols="12" md="7">
        <h2 class="text-h5 mb-4 pl-2">Мои сданные работы</h2>
        
        <v-card v-if="mySubmissions.length === 0" class="pa-6 text-center border-dashed">
          <span class="text-medium-emphasis">Вы еще ничего не сдавали</span>
        </v-card>

        <v-card v-else class="pa-0" border>
          <v-table hover>
            <thead>
              <tr>
                <th class="text-left">ID</th>
                <th class="text-left">Задание / Вариант</th>
                <th class="text-left">Дата</th>
                <th class="text-left">Статус</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sub in mySubmissions" :key="sub.id">
                <td>#{{ sub.id }}</td>
                <td>
                  <div class="font-weight-bold">
                     {{ sub.variant ? sub.variant.description : 'Вариант удален' }}
                  </div>
                </td>
                <td class="text-caption">{{ formatDate(sub.submitted_at) }}</td>
                <td><v-chip color="success" size="small">Сдано</v-chip></td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({ 
    variants: [], 
    mySubmissions: [],
    selectedVariant: null, 
    content: '',
    loading: false
  }),
  
  async mounted() {
    this.fetchData();
  },

  methods: {
    async fetchData() {
      const token = localStorage.getItem('auth_token');
      const config = { headers: { Authorization: `Token ${token}` } };

      try {

        const tasksRes = await axios.get('http://127.0.0.1:8000/api/assignments/', config);
        

        this.variants = tasksRes.data.flatMap(task => 
          task.variants.map(v => ({
            id: v.id,
            label: `${task.title} — ${v.description}`
          }))
        );


        const subsRes = await axios.get('http://127.0.0.1:8000/api/submissions/', config);
        this.mySubmissions = subsRes.data;

      } catch (e) {
        console.error("Ошибка загрузки:", e);
      }
    },

    async submitWork() {
      if (!this.selectedVariant) return alert("Выберите вариант!");
      
      this.loading = true;
      const token = localStorage.getItem('auth_token');
      try {
        await axios.post('http://127.0.0.1:8000/api/submissions/', 
          { variant: this.selectedVariant, content: this.content },
          { headers: { Authorization: `Token ${token}` } }
        );

        this.content = '';
        this.selectedVariant = null;
        await this.fetchData(); 
        alert('Работа принята!');
      } catch (e) {
        alert('Ошибка отправки');
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleString('ru-RU');
    }
  }
}
</script>