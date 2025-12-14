<template>
  <v-container class="mt-4">
    <v-row>
      <!-- Левая колонка: Фильтры -->
      <v-col cols="12" md="4">
        <v-card class="glass-card pa-6 h-100 d-flex flex-column" rounded="xl" elevation="10">
          <div>
            <div class="d-flex align-center mb-6">
              <v-icon icon="mdi-filter-variant" color="secondary" size="24" class="mr-2"></v-icon>
              <span class="text-h6 font-weight-bold">Параметры поиска</span>
            </div>
            
            <p class="text-body-2 text-grey-lighten-1 mb-8" style="line-height: 1.6;">
              Используйте этот инструмент для выявления неэффективных маршрутов. Установите порог заполняемости, чтобы найти проблемные рейсы.
            </p>
            
            <div class="slider-container pa-4 mb-4">
              <div class="d-flex justify-space-between mb-2">
                <span class="text-caption font-weight-bold text-uppercase text-secondary">Макс. Загрузка</span>
                <span class="text-h6 font-weight-bold text-white">{{ (occupancyThreshold * 100).toFixed(0) }}%</span>
              </div>
              
              <v-slider
                v-model="occupancyThreshold"
                min="0"
                max="1"
                step="0.05"
                color="secondary"
                track-color="rgba(255,255,255,0.1)"
                thumb-size="20"
                elevation="2"
              ></v-slider>
            </div>
          </div>

          <v-spacer></v-spacer>

          <v-btn 
            block 
            color="white"
            variant="flat"
            size="large" 
            class="action-btn text-primary font-weight-bold mt-4" 
            @click="pickRoutes"
            :loading="loading"
          >
            Анализировать
          </v-btn>
        </v-card>
      </v-col>

      <!-- Правая колонка: Результаты -->
      <v-col cols="12" md="8">
        <v-card class="glass-card pa-0 h-100" rounded="xl" elevation="10" style="min-height: 500px;">
          <div class="pa-6 border-bottom">
            <h2 class="text-h6 font-weight-bold">Результаты анализа</h2>
            <span class="text-caption text-grey">Найдено рейсов: {{ pickedFlights.length }}</span>
          </div>

          <v-list bg-color="transparent" class="pa-2" lines="two">
            <template v-for="(flight, index) in pickedFlights" :key="flight.id">
              <v-list-item class="flight-item ma-2 rounded-lg">
                <template v-slot:prepend>
                  <div class="flight-number-box mr-4">
                    <span class="text-caption text-grey d-block">Рейс</span>
                    <span class="text-h6 font-weight-bold text-white">{{ flight.id }}</span>
                  </div>
                </template>
                
                <v-list-item-title class="text-white text-body-1 font-weight-medium mb-1 d-flex align-center">
                  {{ flight.departure_airport }} 
                  <v-icon icon="mdi-airplane" size="small" class="mx-3 text-grey rotate-90"></v-icon> 
                  {{ flight.destination_airport }}
                </v-list-item-title>
                
                <v-list-item-subtitle class="text-grey">
                  <v-icon start size="small" icon="mdi-calendar"></v-icon>
                  {{ new Date(flight.departure_time).toLocaleDateString() }}
                </v-list-item-subtitle>
                
                <template v-slot:append>
                  <v-chip color="error" variant="flat" size="small" class="font-weight-bold">
                    Low Occupancy
                  </v-chip>
                </template>
              </v-list-item>
            </template>

            <div v-if="!pickedFlights.length && !loading" class="empty-placeholder d-flex flex-column align-center justify-center h-100">
              <v-icon icon="mdi-radar" size="80" color="rgba(255,255,255,0.1)"></v-icon>
              <p class="text-grey mt-4">Ожидание параметров поиска...</p>
            </div>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';

const occupancyThreshold = ref(0.5);
const pickedFlights = ref([]);
const loading = ref(false);

const pickRoutes = async () => {
  loading.value = true;
  try {
    const res = await api.post('/air/routes/pick/', {
      filled_less_than: occupancyThreshold.value
    });
    pickedFlights.value = res.data.flights;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.glass-card {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.slider-container {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.border-bottom {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.flight-item {
  transition: all 0.2s;
  border: 1px solid transparent;
}

.flight-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.flight-number-box {
  background: rgba(0, 0, 0, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  text-align: center;
  min-width: 80px;
}

.rotate-90 {
  transform: rotate(90deg);
}

.empty-placeholder {
  min-height: 300px;
}

.action-btn {
  transition: transform 0.2s;
}

.action-btn:active {
  transform: scale(0.98);
}
</style>
