<template>
  <v-container fluid class="mt-4 px-4 px-md-8">
    <v-row>
      <v-col cols="12">
        <v-card class="glass-card pa-6" elevation="10" rounded="xl">

          <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between mb-6 gap-4">
            <div class="d-flex align-center">
              <div class="icon-box mr-4">
                <v-icon icon="mdi-wrench-clock" color="white" size="28"></v-icon>
              </div>
              <div>
                <h1 class="text-h5 font-weight-bold text-white mb-1">Центр обслуживания</h1>
                <p class="text-caption text-grey-lighten-1 mb-0">Мониторинг самолетов, находящихся на ремонте</p>
              </div>
            </div>
            
            <v-btn 
              color="primary" 
              variant="tonal" 
              prepend-icon="mdi-refresh" 
              class="refresh-btn"
              @click="loadRepairPlanes"
              :loading="loading"
            >
              Обновить
            </v-btn>
          </div>

          <div class="table-responsive">
            <v-table class="bg-transparent custom-table">
              <thead>
                <tr>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 100px;">ID Борта</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 150px;">Модель</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 250px;">Владелец (Авиакомпания)</th>
                  <th class="text-left text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 150px;">Тех. данные</th>
                  <th class="text-right text-uppercase text-caption font-weight-bold text-blue-grey-lighten-3" style="min-width: 120px;">Статус</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="plane in repairPlanes" :key="plane.id" class="table-row">
                  <td class="font-weight-bold text-white">#{{ plane.id }}</td>
                  
                  <td>
                    <v-chip color="cyan" variant="outlined" size="small" class="font-weight-bold">
                      <v-icon start icon="mdi-airplane" size="x-small"></v-icon>
                      {{ plane.mark }}
                    </v-chip>
                  </td>
                  
                  <td class="text-grey-lighten-1 text-no-wrap">
                    {{ plane.company }}
                  </td>
                  
                  <td class="text-caption text-grey">
                    Duration: {{ plane.flight_duration }}h
                  </td>

                  <td class="text-right">
                    <div class="d-inline-flex align-center status-badge">
                      <span class="status-dot"></span>
                      REPAIR
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
          
          <div v-if="!loading && repairPlanes.length === 0" class="empty-state">
            <v-icon icon="mdi-airplane-check" size="64" color="success" class="mb-4 opacity-50"></v-icon>
            <h3 class="text-h6 text-white">Все системы в норме</h3>
            <p class="text-grey">В данный момент нет самолетов на ремонте</p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const repairPlanes = ref([]);
const loading = ref(false);

const loadRepairPlanes = async () => {
  loading.value = true;
  try {
    const res = await api.get('/air/planes/in_repair/');
    repairPlanes.value = res.data.planes;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(loadRepairPlanes);
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
  background: rgba(244, 67, 54, 0.15);
  color: #ff5252;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background-color: #ff5252;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 8px #ff5252;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.gap-4 {
  gap: 1rem;
}
</style>
