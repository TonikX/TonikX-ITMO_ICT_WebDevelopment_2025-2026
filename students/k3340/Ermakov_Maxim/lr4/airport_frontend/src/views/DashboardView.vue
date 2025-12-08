<template>
  <div class="page">
    <div class="header-row">
      <h1>Панель управления</h1>

      <div v-if="companies.length" class="company-selector">
        <v-select
          v-model="selectedCompanyId"
          :items="companies"
          item-title="name"
          item-value="id"
          label="Авиакомпания"
          density="comfortable"
          variant="outlined"
          hide-details
          style="min-width: 260px"
          @update:model-value="loadDashboardData"
        />
      </div>
    </div>

    <div v-if="!companies.length && !loading" class="error">
      Не удалось загрузить список авиакомпаний.
    </div>

    <div v-if="loading">Загружаем данные...</div>

    <div v-else>
      <v-row class="mt-4" dense align="stretch">
        <!-- Самолёты в ремонте -->
        <v-col cols="12" md="3">
          <v-card class="pa-4 h-100" elevation="2" hover @click="openMaintenanceModal">
            <v-card-title class="text-h6">Самолёты в ремонте</v-card-title>
            <v-card-text>
              <div class="value">{{ planesInMaintenance }}</div>
              <p class="hint mt-2">
                Нажмите, чтобы посмотреть и отредактировать список бортов в
                ремонте для выбранной авиакомпании
              </p>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Количество сотрудников -->
        <v-col cols="12" md="3">
          <v-card class="pa-4 h-100" elevation="2" hover @click="goToStaff">
            <v-card-title class="text-h6">Количество сотрудников</v-card-title>
            <v-card-text>
              <div class="value">{{ employeesCount }}</div>
              <p class="hint mt-2">
                Нажмите, чтобы перейти к списку сотрудников выбранной
                авиакомпании
              </p>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Борта авиакомпании -->
        <v-col cols="12" md="3">
          <v-card class="pa-4 h-100" elevation="2" hover @click="goToFleet">
            <v-card-title class="text-h6">Борта авиакомпании</v-card-title>
            <v-card-text>
              <div class="value">{{ totalPlanes }}</div>
              <p class="hint mt-2">
                Нажмите, чтобы перейти к информации по флоту
              </p>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Популярный самолёт на маршруте -->
        <v-col cols="12" md="3">
          <v-card class="pa-4 h-100" elevation="2">
            <v-card-title class="text-h6">
              Популярный самолёт на маршруте
            </v-card-title>
            <v-card-text>
              <div v-if="topPlaneLoading">Загружаем аналитику...</div>

              <div v-else-if="topPlaneError" class="error">
                {{ topPlaneError }}
              </div>

              <div v-else-if="topPlaneType">
                <div class="value small mb-2">
                  {{ topPlaneType.plane_type_name }}
                </div>
                <p>Рейсов по этому маршруту: {{ topPlaneType.flights_count }}</p>
                <p>Количество мест: {{ topPlaneType.seat_count }}</p>
                <p>Крейсерская скорость: {{ topPlaneType.cruise_speed }} км/ч</p>
              </div>

              <div v-else>
                <p>Для выбранного маршрута пока нет данных.</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <div v-if="error" class="error mt-4">
      {{ error }}
    </div>

    <!-- v-dialog: самолёты и статус ремонта -->
    <v-dialog v-model="showMaintenanceModal" max-width="900">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>Самолёты и статус ремонта</span>
          <v-btn icon="mdi-close" variant="text" @click="closeMaintenanceModal" />
        </v-card-title>

        <v-card-subtitle>
          Авиакомпания:
          <strong>{{ currentCompany ? currentCompany.name : "—" }}</strong>
        </v-card-subtitle>

        <v-card-subtitle>
          Сейчас в ремонте:
          <strong>{{ planesInMaintenance }}</strong>
        </v-card-subtitle>

        <v-card-text>
          <div v-if="planesLoading">Загружаем список самолётов...</div>
          <div v-if="planesError" class="error">{{ planesError }}</div>

          <v-table v-if="filteredPlanes.length && !planesLoading">
            <thead>
              <tr>
                <th>ID</th>
                <th>Бортовой номер</th>
                <th>Тип самолёта (id)</th>
                <th>Компания (id)</th>
                <th>Статус</th>
                <th>Действие</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in filteredPlanes" :key="p.id">
                <td>{{ p.id }}</td>
                <td>{{ p.reg_number }}</td>
                <td>{{ p.plane_type }}</td>
                <td>{{ p.company }}</td>
                <td>
                  <span
                    :class="[
                      'status-tag',
                      p.status === 'maintenance'
                        ? 'status-maintenance'
                        : p.status === 'active'
                        ? 'status-active'
                        : 'status-other',
                    ]"
                  >
                    {{ statusLabel(p.status) }}
                  </span>
                </td>
                <td>
                  <v-btn
                    v-if="p.status !== 'maintenance'"
                    size="small"
                    @click="setMaintenanceStatus(p, 'maintenance')"
                  >
                    В ремонт
                  </v-btn>
                  <v-btn
                    v-else
                    size="small"
                    color="success"
                    @click="setMaintenanceStatus(p, 'active')"
                  >
                    В строй
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>

          <div v-else-if="!planesLoading && !planesError">
            Для выбранной авиакомпании самолётов не найдено.
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeMaintenanceModal">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";

const router = useRouter();

// список компаний и выбранная компания
const companies = ref([]);
const selectedCompanyId = ref(null);

// общие состояния
const loading = ref(true);
const error = ref("");

// агрегированные числа для выбранной компании
const planesInMaintenance = ref(0);
const employeesCount = ref(0);
const totalPlanes = ref(0);

// популярный самолёт на маршруте (общая аналитика)
const topPlaneType = ref(null);
const topPlaneLoading = ref(false);
const topPlaneError = ref("");
const popularRouteId = ref(1); // маршрут, по которому смотрим популярный самолёт

// самолёты для модалки (все, потом фильтруем по компании)
const showMaintenanceModal = ref(false);
const planes = ref([]);
const planesLoading = ref(false);
const planesError = ref("");

// вычисляем текущую компанию
const currentCompany = computed(
  () => companies.value.find((c) => c.id === selectedCompanyId.value) || null
);

// самолёты только выбранной компании
const filteredPlanes = computed(() => {
  if (!selectedCompanyId.value) return [];
  return planes.value.filter((p) => p.company === selectedCompanyId.value);
});

const statusLabel = (status) => {
  if (status === "maintenance") return "В ремонте";
  if (status === "active") return "В строю";
  if (status === "retired") return "Списан";
  return status;
};

const loadCompanies = async () => {
  try {
    const resp = await api.get("/api/companies/");
    companies.value = resp.data || [];
    if (!selectedCompanyId.value && companies.value.length) {
      selectedCompanyId.value = companies.value[0].id;
    }
  } catch (e) {
    console.error(e);
  }
};

const loadPlanes = async () => {
  planesLoading.value = true;
  planesError.value = "";
  try {
    const resp = await api.get("/api/planes/");
    planes.value = resp.data || [];
  } catch (e) {
    console.error(e);
    planesError.value = "Не удалось загрузить список самолётов.";
  } finally {
    planesLoading.value = false;
  }
};

// Главная функция загрузки данных панели
const loadDashboardData = async () => {
  if (!selectedCompanyId.value) return;

  loading.value = true;
  error.value = "";
  topPlaneError.value = "";
  topPlaneType.value = null;

  try {
    // 1. Загружаем список самолётов (для модалки и расчёта ремонта)
    await loadPlanes();

    // 2. Самолёты в ремонте только для выбранной компании
    const planesForCompany = planes.value.filter(
      (p) => p.company === selectedCompanyId.value
    );
    planesInMaintenance.value = planesForCompany.filter(
      (p) => p.status === "maintenance"
    ).length;

    // 3. Кол-во сотрудников для выбранной компании
    const employeesResp = await api.get(
      `/api/companies/${selectedCompanyId.value}/employees-count/`
    );
    employeesCount.value = employeesResp.data.active_employees ?? 0;

    // 4. Флот авиакомпании (общее количество бортов)
    const planesReportResp = await api.get(
      `/api/companies/${selectedCompanyId.value}/planes-report/`
    );
    totalPlanes.value = planesReportResp.data.total_planes ?? 0;

    // 5. Популярный самолёт на маршруте (общая аналитика)
    topPlaneLoading.value = true;
    try {
      const topPlaneResp = await api.get(
        `/api/routes/${popularRouteId.value}/top-plane-type/`
      );
      topPlaneType.value = topPlaneResp.data;
    } catch (e) {
      console.error(e);
      topPlaneError.value =
        "Не удалось загрузить данные по популярному самолёту.";
    } finally {
      topPlaneLoading.value = false;
    }
  } catch (e) {
    console.error(e);
    error.value = "Ошибка при загрузке данных панели управления.";
  } finally {
    loading.value = false;
  }
};

const openMaintenanceModal = async () => {
  showMaintenanceModal.value = true;
  if (!planes.value.length) {
    await loadPlanes();
  }
};

const closeMaintenanceModal = () => {
  showMaintenanceModal.value = false;
};

const setMaintenanceStatus = async (plane, newStatus) => {
  try {
    await api.patch(`/api/planes/${plane.id}/`, {
      status: newStatus,
    });

    await loadDashboardData();
  } catch (e) {
    console.error(e);
    alert("Не удалось обновить статус самолёта.");
  }
};

const goToFleet = () => {
  router.push("/fleet");
};

const goToStaff = () => {
  router.push("/staff");
};

onMounted(async () => {
  await loadCompanies();
  if (selectedCompanyId.value) {
    await loadDashboardData();
  } else {
    loading.value = false;
  }
});
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.value {
  font-size: 32px;
  font-weight: 700;
}

.value.small {
  font-size: 22px;
}

.hint {
  font-size: 13px;
  color: #666;
}

.error {
  color: #d32f2f;
}

.status-tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.status-maintenance {
  background-color: #ffebee;
  color: #c62828;
}

.status-active {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-other {
  background-color: #eceff1;
  color: #455a64;
}
</style>