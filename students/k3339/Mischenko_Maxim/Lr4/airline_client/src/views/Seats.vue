<template>
  <v-container class="fill-height align-start mt-4 justify-center">
    <div style="width: 100%; max-width: 600px;">

      <v-card class="glass-card pa-6 mb-6" rounded="xl" elevation="10">
        <h2 class="text-h5 font-weight-bold text-center mb-6">Поиск свободных мест</h2>
        
        <v-form @submit.prevent="checkSeats" class="d-flex gap-4">
          <v-text-field 
            v-model="flightIdSearch" 
            label="Введите номер рейса (ID)" 
            variant="solo-filled" 
            bg-color="rgba(255,255,255,0.05)"
            prepend-inner-icon="mdi-airplane-search"
            hide-details
            class="flex-grow-1"
            rounded="lg"
            type="number"
          ></v-text-field>
          
          <v-btn 
            type="submit"
            color="secondary" 
            height="56" 
            width="56" 
            icon="mdi-arrow-right"
            rounded="lg"
            elevation="4"
          ></v-btn>
        </v-form>
      </v-card>

      <v-expand-transition>
        <div v-if="searchPerformed" class="plane-container mx-auto">
          
          <div v-if="availableSeats.length > 0">
            <div class="d-flex justify-space-between align-center mb-4 px-4">
              <v-chip color="success" size="small" variant="flat">Доступно: {{ availableSeats.length }}</v-chip>
            </div>

            <div class="fuselage">
              <div class="cockpit"></div>
              
              <div class="cabin-grid">
                <div class="row-indicators mb-2">
                  <span>A</span><span>B</span>
                  <span class="aisle-gap"></span>
                  <span>C</span><span>D</span>
                </div>

                <div class="seats-wrapper">
                   <div 
                    v-for="seat in availableSeats" 
                    :key="seat" 
                    class="seat-unit"
                    v-ripple
                  >
                    {{ seat }}
                  </div>
                </div>
              </div>
              
              <div class="wings left-wing"></div>
              <div class="wings right-wing"></div>
            </div>
          </div>

          <v-alert 
            v-else 
            type="warning" 
            variant="tonal" 
            icon="mdi-alert-circle"
            class="glass-alert mt-4"
            border="start"
          >
            Места не найдены. Проверьте ID рейса или мест нет.
          </v-alert>

        </div>
      </v-expand-transition>
      
    </div>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';

const flightIdSearch = ref('');
const availableSeats = ref([]);
const searchPerformed = ref(false);

const checkSeats = async () => {
  if (!flightIdSearch.value) return;
  searchPerformed.value = true;
  availableSeats.value = [];
  
  try {
    const res = await api.get(`/air/flights/${flightIdSearch.value}/available_seats/`);
    availableSeats.value = res.data.available_seats;
  } catch (e) {
    console.error(e);
  }
};
</script>

<style scoped>
.glass-card {
  background: rgba(30, 41, 59, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.glass-alert {
  background: rgba(255, 152, 0, 0.1) !important;
  border-color: rgba(255, 152, 0, 0.5) !important;
  color: #ffb74d !important;
}

.plane-container {
  perspective: 1000px;
}

.fuselage {
  position: relative;
  background: #E0E7FF;
  padding: 50px 25px 30px 25px;
  border-radius: 60px 60px 20px 20px;
  box-shadow: 
    0 20px 50px rgba(0,0,0,0.5),
    inset 0 0 40px rgba(0,0,0,0.1);
  border: 8px solid #334155;
  margin-top: 20px;
}

.cockpit {
  position: absolute;
  top: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 25px;
  background: #334155;
  border-radius: 10px;
  box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
}

.row-indicators {
  display: flex;
  justify-content: space-between;
  color: #64748B;
  font-weight: bold;
  padding: 0 10px;
  font-size: 0.8rem;
}

.aisle-gap {
  width: 20px;
}

.seats-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
  gap: 10px;
  justify-content: center;
}

.seat-unit {
  background: linear-gradient(180deg, #4ade80 0%, #22c55e 100%);
  color: white;
  padding: 10px 4px;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  font-size: 0.85rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  border-bottom: 3px solid #16a34a;
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
}

.seat-unit:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 10px 15px rgba(34, 197, 94, 0.4);
  z-index: 10;
}

.seat-unit:active {
  transform: translateY(0);
}

.wings {
  position: absolute;
  top: 40%;
  width: 40px;
  height: 100px;
  background: #475569;
  z-index: -1;
  opacity: 0.8;
}

.left-wing {
  left: -45px;
  transform: skewY(30deg);
  border-radius: 10px 0 0 10px;
}

.right-wing {
  right: -45px;
  transform: skewY(-30deg);
  border-radius: 0 10px 10px 0;
}
</style>
