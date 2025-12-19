<template>
  <v-container fluid class="mt-4 px-4 px-md-8">
    <v-row>
      <v-col cols="12">
        <v-card class="glass-card pa-6" elevation="10" rounded="xl">
          <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between mb-6 gap-4">
            <div class="d-flex align-center">
              <div class="icon-box mr-4">
                <v-icon icon="mdi-ticket-account" color="white" size="28"></v-icon>
              </div>
              <div>
                <h1 class="text-h5 font-weight-bold text-white mb-1">Мои билеты</h1>
                <p class="text-caption text-grey-lighten-1 mb-0">Список забронированных авиабилетов</p>
              </div>
            </div>
            
            <v-btn 
              color="primary" 
              variant="tonal" 
              prepend-icon="mdi-refresh" 
              class="refresh-btn"
              @click="loadMyTickets"
              :loading="loading"
            >
              Обновить
            </v-btn>
          </div>

          <div class="table-responsive">
            <v-table class="bg-transparent custom-table">
              <thead>
                <tr>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 100px;">ID Билета</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 150px;">Рейс</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 150px;">Место</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 200px;">Пассажир</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 120px;">Канал продажи</th>
                  <th class="text-right text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 120px;">Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ticket in myTickets" :key="ticket.id" class="table-row">
                  <td class="font-weight-bold text-white">#{{ ticket.id }}</td>
                  
                  <td>
                    <v-chip color="blue" variant="outlined" size="small" class="font-weight-bold">
                      <v-icon start icon="mdi-airplane" size="x-small"></v-icon>
                      Рейс {{ ticket.flight }}
                    </v-chip>
                  </td>
                  
                  <td>
                    <v-chip color="green" variant="outlined" size="small" class="font-weight-bold">
                      <v-icon start icon="mdi-seat-passenger" size="x-small"></v-icon>
                      {{ ticket.seat }}
                    </v-chip>
                  </td>
                  
                  <td class="text-grey-lighten-1 text-no-wrap">
                    {{ ticket.passenger }}
                  </td>
                  
                  <td class="text-grey">
                    {{ ticket.sale_channel }}
                  </td>
                  
                  <td class="text-right">
                    <div class="d-inline-flex align-center status-badge confirmed">
                      <span class="status-dot"></span>
                      {{ ticket.status }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
          
          <div v-if="!loading && myTickets.length === 0" class="empty-state">
            <v-icon icon="mdi-ticket" size="64" color="grey" class="mb-4 opacity-50"></v-icon>
            <h3 class="text-h6 text-white">Билеты не найдены</h3>
            <p class="text-grey">У вас пока нет забронированных авиабилетов</p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const myTickets = ref([]);
const loading = ref(false);

const loadMyTickets = async () => {
  loading.value = true;
  try {
    const res = await api.get('/air/tickets/my_booked/');
    myTickets.value = res.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(loadMyTickets);
</script>

<style scoped>
.glass-card {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.icon-box {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-transparent {
  background: transparent !important;
}

.table-responsive {
  overflow-x: auto;
}

.custom-table th {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
  white-space: nowrap;
}

.custom-table td {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  height: 64px !important;
}

.text-no-wrap {
  white-space: nowrap;
}

.table-row {
  transition: background 0.2s;
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.03) !important;
}

.status-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.status-badge.confirmed {
  background: rgba(76, 175, 80, 0.15);
  color: #4caf50;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 8px currentColor;
}

.status-badge.confirmed .status-dot {
  background-color: #4caf50;
  box-shadow: 0 0 8px #4caf50;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.gap-4 {
  gap: 1rem;
}
</style>