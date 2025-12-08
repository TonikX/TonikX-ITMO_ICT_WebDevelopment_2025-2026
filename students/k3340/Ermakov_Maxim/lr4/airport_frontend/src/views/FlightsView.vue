<template>
  <div class="page">
    <h1>Рейсы и вылеты</h1>

    <!-- 🔵 Аналитика: недозаполненные вылеты -->
    <section class="section">
      <h2>Аналитика: недозаполненные вылеты</h2>

      <!-- Новый красивый FILTER -->
      <v-row class="mb-6" align="center">
        <v-col cols="12" md="6">
          <h3 class="mb-2">Порог заполненности: {{ percent }}%</h3>

          <v-slider
            v-model="percent"
            min="1"
            max="100"
            step="1"
            color="primary"
            thumb-label="always"
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-btn
            color="primary"
            block
            :loading="underfilledLoading"
            @click="loadUnderfilled"
          >
            Показать недозаполненные
          </v-btn>
        </v-col>
      </v-row>

      <p v-if="underfilledError" class="error">{{ underfilledError }}</p>

      <v-table v-if="underfilledItems.length">
        <thead>
          <tr>
            <th>ID вылета</th>
            <th>Номер рейса</th>
            <th>Маршрут</th>
            <th>Заполненность, %</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in underfilledItems" :key="item.flight_instance_id">
            <td>{{ item.flight_instance_id }}</td>
            <td>{{ item.flight_number }}</td>
            <td>{{ item.route }}</td>
            <td>{{ item.occupancy_percent }}</td>
          </tr>
        </tbody>
      </v-table>

      <p v-else-if="!underfilledLoading">
        Недозаполненных вылетов по заданному порогу не найдено.
      </p>
    </section>

    <!-- 🔵 Конкретные вылеты -->
    <section class="section">
      <h2>Конкретные вылеты (FlightInstance)</h2>

      <p v-if="instancesLoading">Загружаем список вылетов...</p>
      <p v-if="instancesError" class="error">{{ instancesError }}</p>

      <v-table v-if="instances.length">
        <thead>
          <tr>
            <th>ID вылета</th>
            <th>Рейс (id)</th>
            <th>Борт (id)</th>
            <th>Статус</th>
            <th>Время вылета</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="fi in instances" :key="fi.id">
            <td>{{ fi.id }}</td>
            <td>{{ fi.flight }}</td>
            <td>{{ fi.plane }}</td>
            <td>{{ fi.status }}</td>
            <td>{{ formatDateTime(fi.departure_time) }}</td>
            <td>
              <v-btn size="small" @click="openFreeSeatsModal(fi)">
                Свободные места
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>

      <p v-else-if="!instancesLoading && !instancesError">
        Вылеты не найдены.
      </p>
    </section>

    <!-- 🔵 Модалка — свободные места -->
    <v-dialog v-model="showFreeSeatsModal" max-width="700">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>
            Свободные места на вылете
            <template v-if="selectedInstance">
              #{{ selectedInstance.id }}
            </template>
          </span>
          <v-btn icon="mdi-close" variant="text" @click="closeFreeSeatsModal" />
        </v-card-title>

        <v-card-subtitle v-if="selectedInstance">
          Рейс (id):
          <strong>{{ selectedInstance.flight }}</strong>,
          борт (id):
          <strong>{{ selectedInstance.plane }}</strong><br />
          Время вылета:
          <strong>{{ formatDateTime(selectedInstance.departure_time) }}</strong>
        </v-card-subtitle>

        <v-card-text>
          <div v-if="freeSeatsLoading">Загружаем список свободных мест...</div>
          <div v-if="freeSeatsError" class="error">{{ freeSeatsError }}</div>

          <div v-if="!freeSeatsLoading && !freeSeatsError">
            <p>
              Свободных мест:
              <strong>{{ freeSeatsCount }}</strong>
            </p>

            <v-table v-if="freeSeats.length">
              <thead>
                <tr>
                  <th>Место</th>
                  <th>Класс</th>
                  <th>Базовая цена</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="seat in freeSeats" :key="seat.id">
                  <td>{{ seat.seat_number }}</td>
                  <td>{{ seat.seat_type }}</td>
                  <td>{{ seat.base_price }}</td>
                </tr>
              </tbody>
            </v-table>

            <p v-else>Свободных мест нет.</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeFreeSeatsModal">
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api/api";

// Аналитика
const percent = ref(70);
const underfilledLoading = ref(false);
const underfilledError = ref("");
const underfilledItems = ref([]);

const loadUnderfilled = async () => {
  underfilledLoading.value = true;
  underfilledError.value = "";
  try {
    const resp = await api.get(
      `/api/analytics/underfilled-routes/?percent=${percent.value}`
    );
    underfilledItems.value = resp.data.items || [];
  } catch (e) {
    console.error(e);
    underfilledError.value = "Ошибка при загрузке данных аналитики.";
  } finally {
    underfilledLoading.value = false;
  }
};

// Вылеты
const instances = ref([]);
const instancesLoading = ref(false);
const instancesError = ref("");

const loadInstances = async () => {
  instancesLoading.value = true;
  instancesError.value = "";
  try {
    const resp = await api.get("/api/flight-instances/");
    instances.value = resp.data || [];
  } catch (e) {
    console.error(e);
    instancesError.value = "Ошибка при загрузке списка вылетов.";
  } finally {
    instancesLoading.value = false;
  }
};

// Модалка свободных мест
const showFreeSeatsModal = ref(false);
const selectedInstance = ref(null);
const freeSeatsLoading = ref(false);
const freeSeatsError = ref("");
const freeSeats = ref([]);
const freeSeatsCount = ref(0);

const openFreeSeatsModal = async (flightInstance) => {
  selectedInstance.value = flightInstance;
  showFreeSeatsModal.value = true;
  await loadFreeSeats(flightInstance.id);
};

const closeFreeSeatsModal = () => {
  showFreeSeatsModal.value = false;
  freeSeats.value = [];
  freeSeatsCount.value = 0;
  freeSeatsError.value = "";
};

const loadFreeSeats = async (id) => {
  freeSeatsLoading.value = true;
  freeSeatsError.value = "";
  try {
    const resp = await api.get(`/api/flight-instances/${id}/free-seats/`);
    freeSeats.value = resp.data.seats || [];
    freeSeatsCount.value = resp.data.free_seats_count ?? freeSeats.value.length;
  } catch (e) {
    console.error(e);
    freeSeatsError.value = "Ошибка при загрузке списка свободных мест.";
  } finally {
    freeSeatsLoading.value = false;
  }
};

const formatDateTime = (d) =>
  d ? new Date(d).toLocaleString() : "";

onMounted(() => {
  loadUnderfilled();
  loadInstances();
});
</script>

<style scoped>
.section {
  margin-bottom: 32px;
}

.error {
  color: #d32f2f;
  margin-top: 8px;
}
</style>