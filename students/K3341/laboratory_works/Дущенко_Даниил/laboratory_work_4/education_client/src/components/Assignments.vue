<template>
  <div>
    <div class="d-flex align-center mb-6">
      <h1 class="text-h4 font-weight-bold">Доступные задания</h1>
      <v-spacer></v-spacer>
    </div>
    
    <v-row>
      <v-col v-for="task in tasks" :key="task.id" cols="12" md="6" lg="4">
        <v-card class="h-100 d-flex flex-column hover-card">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-code-braces" color="primary" class="mr-2"></v-icon>
            </template>
            <v-card-title>{{ task.title }}</v-card-title>
          </v-card-item>

          <v-card-text class="text-medium-emphasis flex-grow-1 pt-2">
            {{ task.description }}
          </v-card-text>
          
          <v-card-actions class="pa-4 pt-0">
            <v-btn to="/submit" variant="tonal" color="primary" block>
              Сдать работу
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Секция преподавателя -->
    <v-divider class="my-10"></v-divider>
    
    <v-card variant="outlined" class="pa-6 border-dashed">
      <h3 class="text-h6 mb-4 d-flex align-center">
        <v-icon icon="mdi-plus-circle-outline" class="mr-2"></v-icon>
        Создать новое задание
      </h3>
      <v-row>
        <v-col cols="12" md="4">
          <v-text-field v-model="newTitle" label="Название задания" bg-color="surface"></v-text-field>
        </v-col>
        <v-col cols="12" md="8">
          <v-text-field v-model="newDesc" label="Краткое описание" bg-color="surface">
            <template v-slot:append>
              <v-btn color="primary" @click="createTask">Создать</v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data: () => ({ tasks: [], newTitle: '', newDesc: '' }),
  async mounted() { this.loadTasks(); },
  methods: {
    async loadTasks() {
      const token = localStorage.getItem('auth_token');
      const res = await axios.get('http://127.0.0.1:8000/api/assignments/', {
        headers: { Authorization: `Token ${token}` }
      });
      this.tasks = res.data;
    },
    async createTask() {
      const token = localStorage.getItem('auth_token');
      await axios.post('http://127.0.0.1:8000/api/assignments/', 
        { title: this.newTitle, description: this.newDesc },
        { headers: { Authorization: `Token ${token}` } }
      );
      this.loadTasks();
    }
  }
}
</script>

<style scoped>
.hover-card:hover {
  transform: translateY(-2px);
  transition: transform 0.2s;
  border-color: #10B981;
}
.border-dashed {
  border-style: dashed !important;
  border-color: rgba(255,255,255,0.2) !important;
}
</style>